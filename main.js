// Initial declarations
let canvas = document.getElementById("canvas");
let ctx = canvas.getContext("2d");
let screenWidth = canvas.width;
let screenHeight = canvas.height;
let populationSize = 5;

tf.setBackend("cpu");
let gen = new Generation(screenWidth, screenHeight, populationSize);

function draw(){
	ctx.fillStyle = 'rgb(176,226,255)';
	ctx.fillRect(0, 0, screenWidth, screenHeight);
	gen.update(ctx);
}

window.requestAnimationFrame(function callback(){
	ctx.clearRect(0, 0, screenWidth, screenHeight);
	draw();
	window.requestAnimationFrame(callback);
});
