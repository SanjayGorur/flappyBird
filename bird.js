class Bird{

	constructor(width, height){
		this.x = width / 4;
		this.y = height / 2;
		this.vy = 0;
		this.vjump = -6;
		this.g = 0.45;
		this.score = 1;
		this.has_collided = false;

	}

	move(){
		this.vy += this.g;
		this.y += this.vy;
	}

	jump(){
		this.vy = this.vjump;
	}

	//think(){
		
	//}

	add_score(){
		this.score += 1;
	}

	draw(ctx){
		ctx.fillRect(this.x, this.y, this.dim, this.dim);
	}


}

module.exports = Bird;
