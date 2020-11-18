function setup() {
  // put setup code here
  //createCanvas(400, 400);
  windowResized();
}

function draw() {
  // put drawing code here
  background(220);
  if (mouseIsPressed) {
    fill(0);
  } else {
    fill(255);
  }
  ellipse(mouseX, mouseY, 80, 80);
}


function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
}
