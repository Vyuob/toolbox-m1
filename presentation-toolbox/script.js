/* ===================================================================
   ToolboxV8 · Soutenance Mastère Cybersécurité
   Navigation + fragments (révélation au clic) + plein écran
   + vue d'ensemble + barre de progression + auto-fit responsive
   + compteurs animés. (Mécanique reprise du modèle presentation-cnil)
   =================================================================== */

(() => {
    const slides = Array.from(document.querySelectorAll('.slide'));
    const total = slides.length;
    let current = 0;

    const $cur = document.getElementById('cur');
    const $total = document.getElementById('total');
    const $speaker = document.getElementById('speaker');
    const $progress = document.getElementById('progress');
    const $prev = document.getElementById('prev');
    const $next = document.getElementById('next');
    const $fs = document.getElementById('fullscreen');
    const $ov = document.getElementById('overview');
    const $ovPanel = document.getElementById('overviewPanel');

    $total.textContent = total;

    /* --- numéro de slide injecté dans le DOM --- */
    slides.forEach((s, idx) => {
        if (!s.classList.contains('cover')) {
            const n = document.createElement('div');
            n.className = 'slide-num';
            n.textContent = String(idx + 1).padStart(2, '0') + ' / ' + String(total).padStart(2, '0');
            s.appendChild(n);
        }
    });

    /* ------------------------------------------------------------------
       Fragments
       ------------------------------------------------------------------ */
    const getFragments = (slide) => Array.from(slide.querySelectorAll('.frag'));
    const getRevealed = (slide) => getFragments(slide).filter(f => f.classList.contains('visible')).length;

    function ensureFragHint(slide) {
        if (slide.classList.contains('cover')) return;
        if (!getFragments(slide).length) return;
        if (!slide.querySelector('.frag-hint')) {
            const hint = document.createElement('div');
            hint.className = 'frag-hint';
            hint.textContent = 'cliquez pour révéler';
            slide.appendChild(hint);
        }
    }
    function refreshFragHint(slide) {
        const frags = getFragments(slide);
        if (frags.length && getRevealed(slide) < frags.length) slide.classList.add('has-pending-frag');
        else slide.classList.remove('has-pending-frag');
    }
    const revealAll = (slide) => { getFragments(slide).forEach(f => f.classList.add('visible')); refreshFragHint(slide); };
    const hideAll = (slide) => { getFragments(slide).forEach(f => f.classList.remove('visible')); refreshFragHint(slide); };

    /* ------------------------------------------------------------------
       Compteurs animés (chiffres clés)
       ------------------------------------------------------------------ */
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const fmt = (n) => n.toLocaleString('fr-FR');
    function animateCounts(slide) {
        slide.querySelectorAll('.count').forEach(el => {
            const target = parseInt(el.dataset.count, 10);
            if (isNaN(target)) return;
            const prefix = el.dataset.prefix || '';
            const suffix = el.dataset.suffix || '';
            if (reduceMotion) { el.textContent = prefix + fmt(target) + suffix; return; }
            const dur = 950, t0 = performance.now();
            const tick = (now) => {
                const p = Math.min((now - t0) / dur, 1);
                const eased = 1 - Math.pow(1 - p, 3); // easeOutCubic
                el.textContent = prefix + fmt(Math.round(target * eased)) + suffix;
                if (p < 1) requestAnimationFrame(tick);
            };
            requestAnimationFrame(tick);
        });
    }

    /* ------------------------------------------------------------------
       Navigation
       ------------------------------------------------------------------ */
    function show(i, opts = {}) {
        if (i < 0) i = 0;
        if (i >= total) i = total - 1;
        const direction = opts.direction || (i >= current ? 'forward' : 'backward');

        slides.forEach((s, idx) => s.classList.toggle('active', idx === i));
        current = i;
        $cur.textContent = i + 1;
        $speaker.textContent = slides[i].dataset.speaker || '';
        if ($progress) $progress.style.width = (((i + 1) / total) * 100) + '%';

        const slide = slides[i];
        ensureFragHint(slide);
        if (direction === 'forward') hideAll(slide);
        else revealAll(slide);
        animateCounts(slide);

        try { sessionStorage.setItem('toolbox-slide', i); } catch (e) {}
    }

    function next() {
        const slide = slides[current];
        const frags = getFragments(slide);
        const revealed = getRevealed(slide);
        if (revealed < frags.length) {
            frags[revealed].classList.add('visible');
            refreshFragHint(slide);
        } else {
            show(current + 1, { direction: 'forward' });
        }
    }
    function prev() {
        const slide = slides[current];
        const revealed = getRevealed(slide);
        if (revealed > 0) {
            getFragments(slide)[revealed - 1].classList.remove('visible');
            refreshFragHint(slide);
        } else {
            show(current - 1, { direction: 'backward' });
        }
    }

    /* ------------------------------------------------------------------
       Auto-fit responsive (slide 1280x720 mise à l'échelle)
       ------------------------------------------------------------------ */
    function fit() {
        const W = 1280, H = 720;
        const s = Math.min(window.innerWidth / W, window.innerHeight / H) * 0.94;
        document.documentElement.style.setProperty('--scale', s.toFixed(3));
    }

    /* ------------------------------------------------------------------
       Plein écran
       ------------------------------------------------------------------ */
    function toggleFullscreen() {
        if (!document.fullscreenElement) document.documentElement.requestFullscreen?.();
        else document.exitFullscreen?.();
    }

    /* ------------------------------------------------------------------
       Vue d'ensemble
       ------------------------------------------------------------------ */
    function buildOverview() {
        $ovPanel.innerHTML = '';
        slides.forEach((s, idx) => {
            const card = document.createElement('div');
            card.className = 'ov-card';
            const title = s.querySelector('h1, h2')?.textContent.trim() || `Slide ${idx + 1}`;
            card.innerHTML = `
                <span class="ov-num">${String(idx + 1).padStart(2, '0')}</span>
                <div class="ov-title">${title}</div>
                <span class="ov-speaker">${s.dataset.speaker || ''}</span>`;
            card.addEventListener('click', () => {
                show(idx, { direction: 'jump' });
                revealAll(slides[idx]);
                $ovPanel.classList.remove('active');
            });
            $ovPanel.appendChild(card);
        });
    }
    function toggleOverview() {
        if (!$ovPanel.children.length) buildOverview();
        $ovPanel.classList.toggle('active');
    }

    /* ------------------------------------------------------------------
       Clavier
       ------------------------------------------------------------------ */
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') { e.preventDefault(); next(); }
        else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); prev(); }
        else if (e.key === 'Home') { e.preventDefault(); show(0, { direction: 'jump' }); revealAll(slides[0]); }
        else if (e.key === 'End') { e.preventDefault(); show(total - 1, { direction: 'jump' }); revealAll(slides[total - 1]); }
        else if (e.key === 'f' || e.key === 'F') { toggleFullscreen(); }
        else if (e.key === 'o' || e.key === 'O') { toggleOverview(); }
        else if (e.key === 'Escape') { $ovPanel.classList.remove('active'); }
    });

    /* ------------------------------------------------------------------
       Tactile (swipe)
       ------------------------------------------------------------------ */
    let tx0 = null;
    document.addEventListener('touchstart', (e) => { tx0 = e.touches[0].clientX; });
    document.addEventListener('touchend', (e) => {
        if (tx0 === null) return;
        const dx = e.changedTouches[0].clientX - tx0;
        if (Math.abs(dx) > 60) (dx < 0 ? next() : prev());
        tx0 = null;
    });

    /* ------------------------------------------------------------------
       Bindings UI + init
       ------------------------------------------------------------------ */
    $next.addEventListener('click', next);
    $prev.addEventListener('click', prev);
    $fs.addEventListener('click', toggleFullscreen);
    $ov.addEventListener('click', toggleOverview);

    window.addEventListener('resize', fit);
    fit();

    slides.forEach(s => { ensureFragHint(s); hideAll(s); });

    let saved = 0;
    try { saved = parseInt(sessionStorage.getItem('toolbox-slide') || '0', 10); } catch (e) {}
    show(Math.min(saved, total - 1), { direction: 'jump' });
})();
