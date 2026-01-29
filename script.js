import './style.css';
import * as THREE from 'three';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );

const renderer = new THREE.WebGLRenderer({ alpha: true });
renderer.setSize( window.innerWidth, window.innerHeight );
renderer.setAnimationLoop( animate );
renderer.render(scene, camera);

const canvas = renderer.domElement;
canvas.style.position = "fixed";
canvas.style.left = "0";
canvas.style.top = "0";
canvas.style.zIndex = "-1";
canvas.style.pointerEvents = "none";
document.body.insertBefore(canvas, document.body.firstChild);
renderer.setClearColor(0x000000, 0);
scene.background = null;

camera.position.z = 26;


function animate() {
  renderer.render( scene, camera );
}

function add_star() {
  const star_geometry = new THREE.SphereGeometry(0.25, 24, 24);
  const star_material = new THREE.MeshBasicMaterial({ color: 0xffffff  });
  const star = new THREE.Mesh(star_geometry, star_material);

  const [x, y, z] = Array(3)
    .fill()
    .map(() => THREE.MathUtils.randFloatSpread(200));

  star.position.set(x, y, z);
  scene.add(star);
}

Array(1000).fill().forEach(add_star);

function moveCamera() {
  const t = document.body.getBoundingClientRect().top;

  camera.position.z = t * -0.01;
  camera.position.x = t * -0.0000;
  camera.rotation.y = t * -0.0000;

}

document.body.onscroll = moveCamera;
moveCamera();

function initMenu() {
  const menuBtn = document.getElementById("menuBtn");
  const sideMenu = document.getElementById("sideMenu");

  console.log("Initializing menu. menuBtn:", menuBtn, "sideMenu:", sideMenu);
  
  if (menuBtn) {
    menuBtn.style.opacity = "1";
  }

  if (menuBtn && sideMenu) {
    menuBtn.addEventListener("click", function(e) {
      e.preventDefault();
      e.stopPropagation();
      console.log("Menu button clicked! Current classes:", sideMenu.className);
      sideMenu.classList.toggle("open");
      console.log("After toggle, classes:", sideMenu.className);
    });
    
    const links = sideMenu.querySelectorAll("a");
    links.forEach(link => {
      link.addEventListener("click", function() {
        sideMenu.classList.remove("open");
      });
    });
  } else {
    console.error("Menu elements not found!");
  }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initMenu);
} else {
  initMenu();
}
