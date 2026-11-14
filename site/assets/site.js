(() => {
  const languageSwitcher = document.querySelector('.language-switcher');
  if (languageSwitcher) {
    const languageOptions = [...languageSwitcher.querySelectorAll('[data-language-option]')];
    const updateLanguageLinks = () => {
      const section = document.getElementById(location.hash.slice(1));
      for (const option of languageOptions) {
        const url = new URL(option.href);
        url.hash = section?.id || '';
        option.href = url.href;
      }
    };
    languageSwitcher.addEventListener('toggle', () => {
      if (languageSwitcher.open) updateLanguageLinks();
    });
    window.addEventListener('hashchange', updateLanguageLinks);
    document.addEventListener('click', event => {
      if (languageSwitcher.open && !languageSwitcher.contains(event.target)) languageSwitcher.open = false;
    });
    languageSwitcher.addEventListener('keydown', event => {
      if (event.key === 'Escape' && languageSwitcher.open) {
        languageSwitcher.open = false;
        languageSwitcher.querySelector('summary').focus();
      }
    });
  }
  const dialog = document.querySelector('#figure');
  if (dialog?.showModal) {
    const image = dialog.querySelector('img');
    const caption = dialog.querySelector('h2');
    const desc = dialog.querySelector('[data-fig-desc]');
    const source = dialog.querySelector('[data-fig-source]');
    let opener;
    for (const link of document.querySelectorAll('[data-figure]')) {
      link.addEventListener('click', e => {
        if (e.metaKey || e.altKey || e.shiftKey || e.ctrlKey) return;
        e.preventDefault();
        opener = link;
        image.src = link.href;
        image.alt = caption.textContent = link.dataset.caption;
        desc.textContent = link.dataset.desc;
        source.href = link.dataset.source;
        dialog.showModal();
        document.documentElement.classList.add('figure-open');
      });
    }
    dialog.querySelector('[data-close]').addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', e => {
      if (e.target !== dialog) return;
      const b = dialog.getBoundingClientRect();
      if (e.clientX < b.left || e.clientX > b.right || e.clientY < b.top || e.clientY > b.bottom) dialog.close();
    });
    dialog.addEventListener('close', () => {
      document.documentElement.classList.remove('figure-open');
      opener?.focus({preventScroll: true});
    });
  }
  const wechat = document.querySelector('#wechat-dialog');
  const wechatLink = document.querySelector('[data-wechat]');
  if (wechat?.showModal && wechatLink) {
    wechatLink.addEventListener('click', event => {
      if (event.metaKey || event.altKey || event.shiftKey || event.ctrlKey) return;
      event.preventDefault();
      wechat.showModal();
    });
    wechat.addEventListener('close', () => wechatLink.focus({preventScroll: true}));
  }
  const widget = document.querySelector('[data-visitor-widget]');
  if (widget) {
    const map = widget.querySelector('img');
    const fallback = document.querySelector('[data-visitor-fallback]');
    const unavailable = document.querySelector('[data-visitor-unavailable]');
    const showBasemap = () => {
      widget.hidden = true;
      fallback.hidden = false;
      unavailable.hidden = false;
    };
    map.addEventListener('error', showBasemap, {once: true});
    if (map.complete && !map.naturalWidth) showBasemap();
  }
  const printCv = document.querySelector('[data-print-cv]');
  if (printCv) {
    const publications = document.querySelectorAll('.academic-cv .cv-bib');
    const openedForPrint = new Set();
    window.addEventListener('beforeprint', () => {
      for (const group of publications) {
        if (group.open) continue;
        openedForPrint.add(group);
        group.open = true;
      }
    });
    window.addEventListener('afterprint', () => {
      for (const group of openedForPrint) group.open = false;
      openedForPrint.clear();
    });
    printCv.addEventListener('click', () => window.print());
    printCv.hidden = false;
  }
  const filters = document.querySelector('#filters');
  if (!filters) return;
  const name = document.querySelector('#find');
  const year = document.querySelector('#year');
  const count = document.querySelector('#count');
  const empty = document.querySelector('#empty');
  const groups = [...document.querySelectorAll('#pub-index .pub-group')];
  const normalize = (s) => s.normalize('NFKC').toLocaleLowerCase();
  const sections = groups.map(el => ({el, rows:[...el.querySelectorAll('.pub-row')].map(row=>({row,text:normalize(row.textContent)}))}));
  function filter(){
    const query = normalize(name.value).trim().split(/\s+/u).filter(Boolean);
    let total = 0;
    for (const {el,rows} of sections) {
      let matches = 0;
      for (const {row,text} of rows) {
        const ok = (!year.value || row.dataset.year === year.value) && query.every(w => text.includes(w));
        row.hidden = !ok;
        if(ok) matches += 1;
      }
      el.hidden = matches === 0;
      total += matches;
    }
    count.textContent = count.dataset.template.replace('{n}', total);
    empty.hidden = total > 0;
  }
  name.addEventListener('input',filter);
  year.addEventListener('change',filter);
  filters.hidden = false;
})();
