/***********************/
let lineLength = 2000;
let elements = 255;
/***********************/

//let dataPointList = new ListArray();
let dataPointList = [];
let counter = 0;

function setup()
{
  windowResized();
  //size(500 ,  700);
  background(255);
  strokeWeight(1);
  noStroke();
  fillBezier();
}

function draw()
{
  drawHorizontalStartLine();
  //noFill();
  fill(0,2);

  if(counter < dataPointList.length)
  {
    changeVisibilityTo(counter);
    drawBezier();
    counter++;
  }
  else
  {
    noLoop();
  }
  //saveFrame(counter + "outputImage.jpg");

}

function changeVisibilityTo(value)
{
  let alphaValue;
  if(value == 0)
  {
    alphaValue = 5;
  }
  else
  {
    alphaValue = value * (255 / dataPointList.length);
  }
  stroke(0, alphaValue);
}

function fillBezier()
{
  for(let i=0; i < elements; i++)
  {
    dataPointList.push(random(0,2000));
  }
}

function drawBezier()
{
  let bezierLength = width - 2 * lineLength;
  let elementWidth = bezierLength / dataPointList.length;
  //noStroke();
  bezier( lineLength,
          height/2.0,

          width/2,
          height/2,

          width/2,
          height/2.0,

          width,
          dataPointList[counter]);
}

function drawHorizontalStartLine()
{
  line(0,height/2.0,lineLength,height/2.0);

}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
}
