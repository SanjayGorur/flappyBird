
class Generation{

	constructor(screenWidth, screenHeight, populationSize){
		this.screenWidth = screenWidth;
		this.screenHeight = screenHeight;
		this.populationSize = populationSize;	
		this.birds = [];
		this.pipes = [];
		for(let i = 0; i < populationSize; i++){
			this.birds.push(new Bird(this.screenWidth, this.screenHeight));
		}
		this.pipes.push(new Pipe(this.screenWidth, this.screenHeight, this.populationSize));
		this.generationNumber = 1;
		this.matingPool = [];
		this.mutationRate = 0.03;
	}
	

	checkCollisions(){
		for(let bird of this.birds){
			for(let pipe of this.pipes){
				// using box method to check collisions
				if((bird.x + bird.width >= pipe.x) && (bird.x <= pipe.x + pipe.width)){
					if(bird.y <= pipe.heightTop){
						bird.hasCollided = true;
						bird.distanceToGap = pipe.heightTop - bird.y;
					}
					else if(bird.y + bird.width >= pipe.heightTop + pipe.gapSize){
						bird.hasCollided = true;
						bird.distanceToGap = bird.y + bird.width - pipe.heightTop - pipe.gapSize;
					}
				}
			}
		}
	}

	updateScores(){
		for(let pipe of this.pipes){
			for(let i = 0; i < this.birds.length; i++){
				let bird = this.birds[i];
				// make sure bird is not double counted for passing same pipe 
				if(!bird.hasCollided && bird.x >= pipe.x + pipe.width && !pipe.hasPassed[i]){
					bird.pipesPassed++;
					pipe.hasPassed[i] = true;
				}
			}
		}
	}
	
	calculateFitness(){
		// weight pipes passed and distanceToGap
		// using softmax distribution
		let norm = 0;
		for(let bird of this.birds){
			bird.score = 0.10 * 1 / (bird.distanceToGap) + 0.90 * bird.pipesPassed;
			norm += Math.exp(bird.score);
		}
		for(let bird of this.birds){
			bird.fitness = Math.exp(bird.score) / norm;
		}
	}

	generateMatingPool(){
		// scale fitnesses
		for(let bird of this.birds){
			let scaledSize = Math.floor(bird.fitness * 1000);
			for(let i = 0; i < scaledSize; i++){
				this.matingPool.push(bird);
			}
		}
	}

	reproduction(){
		let nextBirds = [];
		let matingPoolSize = this.matingPool.length;
		for(let i = 0; i < this.populationSize; i++){
			let parent1 = this.matingPool[Math.floor(Math.random() * matingPoolSize)];
			let parent2 = this.matingPool[Math.floor(Math.random() * matingPoolSize)];
			let child = new Bird(this.screenWidth, this.screenHeight);
			child.crossover(parent1, parent2);
			child.mutate();
			nextBirds.push(child);
				//let child = this.matingPool[Math.floor(Math.random() * matingPoolSize)];
				//child.hasCollided = false;
				//nextBirds.push(child);
		}
		this.birds = nextBirds;

	}



	isGenerationOver(){
		for(let bird of this.birds){
			if(!bird.hasCollided){
				return;
			}
		}
		this.calculateFitness();	
		this.generateMatingPool();
		this.reproduction();
		//for(let bird of this.birds){
			//console.log(bird.model.getWeights());
		//}
		this.pipes = [];
		this.pipes.push(new Pipe(this.screenWidth, this.screenHeight, this.populationSize));
		this.generationNumber++;
		
	}

	move(){
		for(let bird of this.birds){
			// gather neural input
			let input = [];
			for(let pipe of this.pipes){
				if(pipe.x >= bird.x + bird.width){
					input[0] = pipe.x - bird.x;
					input[1] = bird.y;
					input[2] = bird.vy;
					input[3] = pipe.heightTop;
					input[4] = pipe.gapSize;
					break;	
				}
			}
			bird.move(input);
		}
		for(let pipe of this.pipes){
			pipe.move();
		}
	}	

	draw(ctx){
		ctx.fillStyle = "black";
		ctx.fillText("Generation: " + this.generationNumber, 10, 10);
		ctx.fillStyle = "forestgreen";
		for(let bird of this.birds){
			if(!bird.hasCollided){
				ctx.fillRect(bird.x, bird.y, bird.width, bird.width);
			}
		}
		for(let pipe of this.pipes){
			ctx.fillRect(pipe.x, 0, pipe.width, pipe.heightTop);
			ctx.fillRect(pipe.x, pipe.heightTop + pipe.gapSize, pipe.width, pipe.heightBottom);
		}
	}
	
	pipeMaintain(){
		for(let pipe of this.pipes){
			if(!pipe.hasAdded && pipe.x <= Math.floor(this.screenWidth * 3/5)){
				this.pipes.push(new Pipe(this.screenWidth, this.screenHeight));
				pipe.hasAdded = true;
			}
		}
		if(this.pipes[0].x + this.pipes[0].width <= 0){
			this.pipes.shift();
		}
	}

	update(ctx){
		this.move();
		this.checkCollisions();
		this.updateScores();
		this.pipeMaintain();
		this.isGenerationOver();
		this.draw(ctx);
	}

}
