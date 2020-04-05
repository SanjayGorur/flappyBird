class Pipe{
	constructor(screenWidth, screenHeight, populationSize){
		this.width = 60;
		this.gapSize = 170;
		this.buffer = 30;
		this.minHeight = 40;
		this.heightTop = Math.floor(Math.random() * (screenHeight - this.gapSize - this.minHeight));
		this.heightBottom = screenHeight - this.gapSize - this.heightTop;
		this.x = screenWidth + this.width + this.buffer;
		this.vx = -4;
		this.hasPassed = [];
		for(let i = 0; i < populationSize; i++){
			this.hasPassed[i] = false;
		}
		this.hasAdded = false;
	}

	move(){
		this.x += this.vx;
	}

}

