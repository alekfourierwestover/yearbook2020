
const numconfettis = 1000;
const numcolors = 5;
let confettis = [];
let ww = window.innerWidth;
let wh = window.innerHeight;

let pos = [];
let vels = [];

let wind_force = {"x": 0, "y": 0};

const gravity = 0.0001;
const dt = 60;
const wind_period = 0.2;

const initial_down_vel = 2;
let tick_ct = 0;
let wind_xoff = wind_period*Math.PI*2 *Math.random();
let wind_yoff = wind_period*Math.PI*2 *Math.random();

setTimeout(()=>{
for (var i = 0; i < numconfettis; i++) {
  let color_i = Math.floor(Math.random()*numcolors);
  let size_i = 5*Math.random()+5;

  wh = Math.max($(document).height(), wh);

  confettis.push($(`<div class="confetti confetti${color_i}"></div>`));

  confettis[i].width(size_i);
  confettis[i].height(size_i);
  vels.push({"x": .6*(Math.random()-0.5), "y": initial_down_vel*Math.random()});
  $("#confetti-place").append(confettis[i]);
  pos.push({"x": Math.random()*ww, "y": Math.random()*wh*0.01});
  $(confettis[i]).css({top: pos[i].y, left: pos[i].x});
}
update();

}, 1000);

function update(){
  tick_ct += 1;

  wind_force.x = 0.1*Math.sign(Math.sin(tick_ct*wind_period+wind_xoff))*Math.pow(Math.sin(tick_ct*wind_period+wind_xoff), 6);

  for (var i = confettis.length-1; i >= 0; i--) {
    vels[i].y += gravity*dt;

    vels[i].y += wind_force.y*dt;

    pos[i].x += (vels[i].x+wind_force.x)*dt;
    pos[i].y += vels[i].y*dt;
    $(confettis[i]).css({top: pos[i].y, left: pos[i].x});

    if(pos[i].y >= wh || pos[i].x >= ww || pos[i].x < 0){
      confettis[i].remove();

      pos.splice(i,1);
      vels.splice(i,1);
      confettis.splice(i,1);
    }
  }
  if(confettis.length > 0){
    setTimeout(update, dt);
  }
}
