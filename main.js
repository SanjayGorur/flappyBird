const Bird = require("./bird.js");

let canvas = document.getElementById("canvas");
let ctx = canvas.getContext("2d");
let width = canvas.width;
let height = canvas.height;
ctx.fillStyle = 'rgb(176,226,255)';
ctx.fillRect(0, 0, width, height);

let bird = new Bird(width, height);
document.write("ello");
document.write(bird.x);
ctx.fillRect(bird.x, bird.y, bird.dim, bird.dim);
