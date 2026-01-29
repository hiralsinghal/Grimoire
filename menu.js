(function(){
  function init() {
    const menuBtn = document.getElementById('menuBtn');
    const sideMenu = document.getElementById('sideMenu');
    if (!menuBtn) return console.warn('menuBtn not found');
    if (!sideMenu) return console.warn('sideMenu not found');

    menuBtn.addEventListener('click', function(e){
      e.preventDefault();
      e.stopPropagation();
      sideMenu.classList.toggle('open');
      console.log('menu toggled ->', sideMenu.classList.contains('open'));
    });

    sideMenu.querySelectorAll && sideMenu.querySelectorAll('a').forEach(function(a){
      a.addEventListener('click', function(){ sideMenu.classList.remove('open'); });
    });

    document.addEventListener('click', function(e){
      const target = e.target;
      const isClickInsideMenu = sideMenu.contains(target) || menuBtn.contains(target);
      if (!isClickInsideMenu && sideMenu.classList.contains('open')) {
        sideMenu.classList.remove('open');
        console.log('menu closed by outside click');
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();