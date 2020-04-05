
class Bird{

	constructor(screenWidth, screenHeight){
		this.screenWidth = screenWidth;
		this.screenHeight = screenHeight;
		this.x = Math.floor(this.screenWidth / 5);
		this.y = Math.floor(this.screenHeight / 3);
		this.vy = 0;
		this.vJump = -6;
		this.g = 0.45;
		this.pipesPassed = 0;
		this.hasCollided = false;
		this.distanceToGap = 0;
		this.width = 30;
		this.fitness = 0;
		// model
		this.brain = new NeuralNetwork(5, 3, 2);
	}

	jump(){
		this.vy = this.vJump;
	}

	think(input){
		let predictions = this.brain.predict(input);
		if(predictions[0] > predictions[1])
			this.jump();
	}

	move(input){
		this.vy += this.g;
		this.y += this.vy;
		this.think(input);
		if(this.y <= 0){
			this.y = 0;
		}
		else if(this.y >= this.screenHeight){
			this.y = this.screenHeight - 20;
		}
	}

	add_score(){
		this.score += 1;
	}

	crossover(parent1, parent2){
		this.brain.crossover(parent1.brain, parent2.brain);
	}

	mutate(mutationRate){
		this.brain.mutate(mutationRate);
	}

	//draw(ctx){
		//ctx.fillStyle = "forestgreen";
		//ctx.fillRect(this.x, this.y, this.dim, this.dim);
	//}

}

