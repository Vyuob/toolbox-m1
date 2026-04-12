"""
Générateur de Rapports
-----------------------
Produit des rapports en PDF, HTML et CSV à partir des résultats de scan.
Utilise Jinja2 pour le rendu et WeasyPrint pour la conversion PDF.
Stocke les fichiers dans MinIO.
"""

import csv
import io
import logging
import os
import tempfile
from datetime import datetime

from jinja2 import Environment, FileSystemLoader

from app.core.config import settings

logger = logging.getLogger(__name__)

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "templates")
REPORTS_DIR   = "/tmp/reports"
os.makedirs(REPORTS_DIR, exist_ok=True)


class ReportGenerator:
    def __init__(self):
        self.jinja_env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), autoescape=True)

    def generate(self, scan_job_id: int, fmt: str, user_id: int) -> str:
        from app.core.database import SessionLocal
        from app.models.scan import ScanJob, Report

        db = SessionLocal()
        try:
            # Import all models so SQLAlchemy metadata knows all tables
            from app.models.user import User  # noqa: F401
            job = db.query(ScanJob).filter(ScanJob.id == scan_job_id).first()
            if not job:
                raise ValueError(f"ScanJob #{scan_job_id} introuvable")

            # job.result peut être {"data": {...}, "logs": [...]} ou directement les données
            raw = job.result or {}
            result_data = raw.get("data", raw) if isinstance(raw, dict) and "data" in raw else raw

            context = {
                "title": f"Rapport Pentest – {job.module.upper()} sur {job.target}",
                "generated_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "job": job,
                "result": result_data if isinstance(result_data, dict) else {},
            }

            if fmt == "pdf":
                path = self._generate_pdf(context, scan_job_id)
            elif fmt == "html":
                path = self._generate_html(context, scan_job_id)
            elif fmt == "csv":
                path = self._generate_csv(context, scan_job_id)
            else:
                raise ValueError(f"Format inconnu : {fmt}")

            report = Report(
                title=context["title"],
                scan_job_id=scan_job_id,
                format=fmt,
                file_path=path,
                created_by=user_id,
            )
            db.add(report)
            db.commit()

            self._upload_to_minio(path)
            return path
        finally:
            db.close()

    def _generate_html(self, context: dict, job_id: int) -> str:
        tpl = self.jinja_env.get_template("report.html")
        html = tpl.render(**context)
        path = os.path.join(REPORTS_DIR, f"rapport_{job_id}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        return path

    def _generate_pdf(self, context: dict, job_id: int) -> str:
        """Génère un vrai PDF structuré avec ReportLab, inspiré du modèle pentest_rapport_generator."""
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
            HRFlowable, KeepTogether,
        )
        from reportlab.lib.enums import TA_LEFT, TA_CENTER

        # Palette inspirée du template exemple
        PRIMARY      = colors.HexColor("#1f3b82")
        PRIMARY_DARK = colors.HexColor("#16306b")
        TEXT         = colors.HexColor("#0b1b2b")
        MUTED        = colors.HexColor("#5c6b7a")
        BORDER       = colors.HexColor("#d7dbe8")
        BG_SOFT      = colors.HexColor("#f6f7fb")
        CODIR_BG     = colors.HexColor("#fff7ed")
        CODIR_BORDER = colors.HexColor("#fb923c")
        CODIR_TEXT   = colors.HexColor("#c2410c")
        CODE_BG      = colors.HexColor("#0f172a")
        CODE_FG      = colors.HexColor("#f8fafc")

        pdf_path = os.path.join(REPORTS_DIR, f"rapport_{job_id}.pdf")
        doc = SimpleDocTemplate(
            pdf_path, pagesize=A4,
            rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2.5*cm,
            title=context["title"], author="PentestBox",
        )

        ss = getSampleStyleSheet()
        eyebrow = ParagraphStyle("eyebrow", parent=ss["Normal"],
            fontSize=7, textColor=MUTED, spaceAfter=4,
            fontName="Helvetica-Bold", leading=9)
        title_st = ParagraphStyle("title", parent=ss["Title"],
            fontSize=22, textColor=PRIMARY, spaceAfter=6,
            alignment=TA_LEFT, fontName="Helvetica-Bold", leading=26)
        subtitle_st = ParagraphStyle("subtitle", parent=ss["Normal"],
            fontSize=10, textColor=MUTED, spaceAfter=10, leading=13)
        h2_st = ParagraphStyle("h2", parent=ss["Heading2"],
            fontSize=14, textColor=PRIMARY, spaceBefore=14, spaceAfter=8,
            fontName="Helvetica-Bold", leading=18,
            borderColor=PRIMARY, borderPadding=(0, 0, 0, 8), leftIndent=10)
        h3_st = ParagraphStyle("h3", parent=ss["Heading3"],
            fontSize=11, textColor=PRIMARY_DARK, spaceBefore=8, spaceAfter=4,
            fontName="Helvetica-Bold", leading=14)
        meta_lbl = ParagraphStyle("metalbl", parent=ss["Normal"],
            fontSize=7, textColor=PRIMARY, fontName="Helvetica-Bold", leading=9)
        meta_val = ParagraphStyle("metaval", parent=ss["Normal"],
            fontSize=9, textColor=TEXT, leading=12)
        body_st = ParagraphStyle("body", parent=ss["Normal"],
            fontSize=9.5, textColor=TEXT, spaceAfter=5, leading=13.5)
        muted_st = ParagraphStyle("muted", parent=ss["Normal"],
            fontSize=8, textColor=MUTED, spaceAfter=5, leading=11)
        code_st = ParagraphStyle("code", parent=ss["Code"],
            fontSize=7.5, textColor=CODE_FG, backColor=CODE_BG,
            borderPadding=8, leading=10.5,
            fontName="Courier", leftIndent=0)
        codir_st = ParagraphStyle("codir", parent=ss["Normal"],
            fontSize=10, textColor=TEXT, leading=14, leftIndent=8, rightIndent=8,
            spaceBefore=4, spaceAfter=4)

        story = []
        job = context["job"]
        result = context.get("result", {}) or {}

        # ── HEADER (cover) ─────────────────────────────────────────
        story.append(Paragraph("PENTESTBOX • RAPPORT AUTOMATISÉ", eyebrow))
        story.append(Paragraph(context["title"], title_st))
        story.append(Paragraph(
            "Audit de sécurité offensif – résultats détaillés et recommandations.",
            subtitle_st))
        story.append(HRFlowable(width="100%", thickness=2, color=PRIMARY,
            spaceBefore=4, spaceAfter=10))

        # Tableau métadonnées (4 colonnes)
        meta_rows = [
            ["CIBLE", "MODULE", "STATUT", "GÉNÉRÉ LE"],
            [str(job.target), str(job.module).upper(), str(job.status), context['generated_at']],
        ]
        meta_t = Table(meta_rows, colWidths=[(17/4)*cm]*4)
        meta_t.setStyle(TableStyle([
            ("BACKGROUND",     (0, 0), (-1, 0), BG_SOFT),
            ("TEXTCOLOR",      (0, 0), (-1, 0), PRIMARY),
            ("FONTNAME",       (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE",       (0, 0), (-1, 0), 7),
            ("FONTSIZE",       (0, 1), (-1, 1), 9),
            ("ALIGN",          (0, 0), (-1, -1), "LEFT"),
            ("VALIGN",         (0, 0), (-1, -1), "MIDDLE"),
            ("BOX",            (0, 0), (-1, -1), 0.5, BORDER),
            ("INNERGRID",      (0, 0), (-1, -1), 0.5, BORDER),
            ("LEFTPADDING",    (0, 0), (-1, -1), 8),
            ("RIGHTPADDING",   (0, 0), (-1, -1), 8),
            ("TOPPADDING",     (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING",  (0, 0), (-1, -1), 6),
        ]))
        story.append(meta_t)
        story.append(Spacer(1, 6))
        story.append(Paragraph(
            "<b>Légende criticité :</b> Info • Low • Medium • High • Critical "
            "(selon CVSS et impact métier).", muted_st))

        # ── SYNTHÈSE CODIR ────────────────────────────────────────
        story.append(Spacer(1, 10))
        codir_title = ParagraphStyle("codir_h", parent=h2_st,
            textColor=CODIR_TEXT, leftIndent=0)
        codir_content = [
            Paragraph("Synthèse exécutive (CODIR)", codir_title),
            Paragraph(
                f"Ce rapport présente les résultats du module <b>{job.module}</b> "
                f"exécuté sur la cible <b>{job.target}</b>. Les sections ci-dessous "
                f"détaillent les outils utilisés, les données collectées et les "
                f"recommandations de remédiation. Les actions urgentes sont listées "
                f"en fin de rapport.", codir_st),
        ]
        codir_box = Table([[c] for c in codir_content], colWidths=[17*cm])
        codir_box.setStyle(TableStyle([
            ("BACKGROUND",   (0, 0), (-1, -1), CODIR_BG),
            ("LINEBEFORE",   (0, 0), (0, -1), 4, CODIR_BORDER),
            ("LEFTPADDING",  (0, 0), (-1, -1), 14),
            ("RIGHTPADDING", (0, 0), (-1, -1), 14),
            ("TOPPADDING",   (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 10),
        ]))
        story.append(codir_box)

        # ── STATISTIQUES ──────────────────────────────────────────
        story.append(Paragraph("Statistiques", h2_st))
        stat_rows = [[
            Paragraph(f"<b><font size=14 color='#1f3b82'>{len(result)}</font></b><br/>"
                      f"<font size=7 color='#5c6b7a'>OUTILS UTILISÉS</font>", body_st),
            Paragraph(f"<b><font size=14 color='#1f3b82'>{job.module.upper()}</font></b><br/>"
                      f"<font size=7 color='#5c6b7a'>MODULE</font>", body_st),
            Paragraph(f"<b><font size=14 color='#1f3b82'>{job.status}</font></b><br/>"
                      f"<font size=7 color='#5c6b7a'>STATUT FINAL</font>", body_st),
        ]]
        stats_t = Table(stat_rows, colWidths=[(17/3)*cm]*3)
        stats_t.setStyle(TableStyle([
            ("BACKGROUND",   (0, 0), (-1, -1), BG_SOFT),
            ("BOX",          (0, 0), (-1, -1), 0.5, BORDER),
            ("INNERGRID",    (0, 0), (-1, -1), 0.5, BORDER),
            ("ALIGN",        (0, 0), (-1, -1), "CENTER"),
            ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING",  (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING",   (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 12),
        ]))
        story.append(stats_t)

        # ── DÉROULÉ TECHNIQUE & PREUVES ───────────────────────────
        story.append(Paragraph("Déroulé technique &amp; preuves", h2_st))
        if not result:
            story.append(Paragraph("<i>Aucune donnée collectée.</i>", body_st))
        else:
            for tool, data in result.items():
                story.append(Paragraph(f"{tool.upper()}", h3_st))
                story.append(Paragraph(
                    f"Résultats produits par l'outil <font face='Courier'>{tool}</font> :",
                    muted_st))
                v_str = str(data)
                if len(v_str) > 1500:
                    v_str = v_str[:1500] + "\n[…] (tronqué)"
                v_str = v_str.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                v_str = v_str.replace("\n", "<br/>")
                story.append(Paragraph(v_str, code_st))
                story.append(Spacer(1, 6))

        # ── TABLEAU SYNTHÉTIQUE ───────────────────────────────────
        story.append(Paragraph("Tableau synthétique", h2_st))
        table_data = [["ID", "Outil", "Type", "Statut"]]
        if result:
            for i, (tool, _) in enumerate(result.items(), start=1):
                table_data.append([
                    f"R-{i:03d}",
                    str(tool),
                    str(job.module),
                    "Collecté",
                ])
        else:
            table_data.append(["—", "—", "—", "—"])

        synth_t = Table(table_data, colWidths=[2.5*cm, 5.5*cm, 4.5*cm, 4.5*cm], repeatRows=1)
        synth_t.setStyle(TableStyle([
            ("BACKGROUND",     (0, 0), (-1, 0), PRIMARY),
            ("TEXTCOLOR",      (0, 0), (-1, 0), colors.white),
            ("FONTNAME",       (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE",       (0, 0), (-1, 0), 9),
            ("FONTSIZE",       (0, 1), (-1, -1), 8.5),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BG_SOFT]),
            ("GRID",           (0, 0), (-1, -1), 0.25, BORDER),
            ("VALIGN",         (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING",    (0, 0), (-1, -1), 8),
            ("RIGHTPADDING",   (0, 0), (-1, -1), 8),
            ("TOPPADDING",     (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING",  (0, 0), (-1, -1), 6),
        ]))
        story.append(synth_t)

        # ── RECOMMANDATIONS ───────────────────────────────────────
        story.append(Paragraph("Recommandations", h2_st))
        recs = [
            ("Correctifs", "appliquer les patches de sécurité pour les vulnérabilités identifiées (CVE)."),
            ("Composants tiers", "mettre à jour les dépendances et bibliothèques signalées."),
            ("Configuration", "renforcer TLS, en-têtes HTTP, désactiver les services obsolètes (Telnet, SMBv1)."),
            ("Surface d'attaque", "restreindre les ports exposés publiquement et appliquer le principe du moindre privilège."),
            ("Validation", "planifier un nouveau test après remédiation pour confirmer les corrections."),
        ]
        for label, txt in recs:
            story.append(Paragraph(f"• <b>{label} :</b> {txt}", body_st))

        # ── ANNEXES ───────────────────────────────────────────────
        story.append(Paragraph("Annexes", h2_st))
        story.append(Paragraph(
            "Les données brutes des outils sont incluses dans la section "
            "« Déroulé technique &amp; preuves » ci-dessus. Les logs d'exécution "
            "complets sont disponibles dans l'interface PentestBox via le bouton "
            "« Voir » du job correspondant.", muted_st))

        # ── FOOTER ────────────────────────────────────────────────
        def _footer(canvas, doc_):
            canvas.saveState()
            canvas.setFont("Helvetica", 7.5)
            canvas.setFillColor(MUTED)
            canvas.drawString(2*cm, 1.2*cm,
                f"PentestBox – Mastère Cybersécurité – {context['generated_at']}")
            canvas.drawRightString(A4[0] - 2*cm, 1.2*cm, f"Page {doc_.page}")
            canvas.setStrokeColor(BORDER)
            canvas.line(2*cm, 1.6*cm, A4[0] - 2*cm, 1.6*cm)
            canvas.restoreState()

        doc.build(story, onFirstPage=_footer, onLaterPages=_footer)
        logger.info(f"PDF généré avec ReportLab : {pdf_path}")
        return pdf_path

    def _generate_csv(self, context: dict, job_id: int) -> str:
        path = os.path.join(REPORTS_DIR, f"rapport_{job_id}.csv")
        result = context.get("result", {})
        rows: list[list] = [["Clé", "Valeur"]]
        for k, v in result.items():
            rows.append([k, str(v)])

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Rapport", context["title"]])
            writer.writerow(["Généré le", context["generated_at"]])
            writer.writerow([])
            writer.writerows(rows)
        return path

    def _upload_to_minio(self, file_path: str) -> bool:
        try:
            from minio import Minio
            client = Minio(
                settings.MINIO_ENDPOINT,
                access_key=settings.MINIO_ACCESS_KEY,
                secret_key=settings.MINIO_SECRET_KEY,
                secure=settings.MINIO_SECURE,
            )
            if not client.bucket_exists(settings.MINIO_BUCKET):
                client.make_bucket(settings.MINIO_BUCKET)
            object_name = os.path.basename(file_path)
            client.fput_object(settings.MINIO_BUCKET, object_name, file_path)
            logger.info(f"Rapport uploadé dans MinIO : {object_name}")
            return True
        except Exception as e:
            logger.warning(f"Upload MinIO échoué : {e}")
            return False
