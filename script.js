import './style.css';
import * as THREE from 'three';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );

const renderer = new THREE.WebGLRenderer()
renderer.setSize( window.innerWidth, window.innerHeight );
renderer.setAnimationLoop( animate );
renderer.render(scene, camera);
document.body.appendChild( renderer.domElement );
scene.background = new THREE.Color( 0x222222 );

camera.position.setZ = 26;

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

document.getElementById("playAudio").addEventListener("click", function(){
    var audio = document.getElementById('audio');
  if(this.className == 'is-playing'){
    this.className = "";
    this.innerHTML = "Play"
    audio.pause();
  }else{
    this.className = "is-playing";
    this.innerHTML = "Pause";
    audio.play();
  }

})