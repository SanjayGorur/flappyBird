// 3-layer NN library  

class NeuralNetwork{
	
	constructor(inputNodes, hiddenNodes, outputNodes){
		this.inputNodes = inputNodes;
		this.hiddenNodes = hiddenNodes;
		this.outputNodes = outputNodes;
		this.weights1 = tf.randomNormal([this.hiddenNodes, this.inputNodes]);
		this.weights2 = tf.randomNormal([this.outputNodes, this.hiddenNodes]);
	}
	
	// input is a 1d array
	predict(input){
		const tensorInput = tf.tensor(input).reshape([this.inputNodes, 1]);
		let output;
		tf.tidy(() => {
			const hiddenActivations = this.weights1.matMul(tensorInput).sigmoid();
			const outputActivations = this.weights2.matMul(hiddenActivations).sigmoid();
			// reshape to 1d
			outputActivations.reshape([1, this.outputNodes]);
			output = outputActivations.dataSync();		
		});
		return output;
	}
	
	clearWeights(){
		this.weights1.dispose();
		this.weights2.dispose();
	}

	clone(){
		let cloneVersion = new NeuralNetwork(this.inputNodes, this.hiddenNodes, this.outputNodes);
		cloneVersion.clearWeights();
		cloneVersion.weights1 = this.weights1;
		cloneVersion.weights2 = this.weights2;
	}

	mutate(mutationRate){
		this.weights1 = tf.tidy(() => {
			const buffer = tf.buffer(this.weights1.shape, this.weights1.dtype, this.weights1.dataSync());
			for(let i = 0; i < this.weights1.shape[0]; i++){
				for(let j = 0; j < this.weights1.shape[1]; j++){
					if(Math.random() < mutationRate)
						buffer.set(Math.random(), i, j);
				}
			}
			return buffer.toTensor();
		});
		this.weights2 = tf.tidy(() => {
			const buffer = tf.buffer(this.weights2.shape, this.weights2.dtype, this.weights2.dataSync());
			for(let i = 0; i < this.weights2.shape[0]; i++){
				for(let j = 0; j < this.weights2.shape[1]; j++){
					if(Math.random() < mutationRate)
						buffer.set(Math.random(), i, j);
				}
			}
			return buffer.toTensor();
		});
	}

	crossover(brainParent1, brainParent2){
		this.clearWeights();
		let dim1 = brainParent1.weights1.shape;
		let sliceRow = Math.floor(Math.random() * dim1[0]) + 1;
		//console.log(sliceRow);
		this.weights1 = tf.tidy(() => {
			const sliceParent1 = brainParent1.weights1.slice([0, 0], [sliceRow, dim1[1]]);
			const sliceParent2 = brainParent2.weights1.slice([sliceRow, 0], [dim1[0] - sliceRow, dim1[1]]);
			return tf.concat([sliceParent1, sliceParent2], 0);
		});
		let dim2 = brainParent1.weights2.shape;
		sliceRow = Math.floor(Math.random() * dim2[0]) + 1;
		this.weights2 = tf.tidy(() => {
			const sliceParent1 = brainParent1.weights2.slice([0, 0], [sliceRow, dim2[1]]);
			const sliceParent2 = brainParent2.weights2.slice([sliceRow, 0], [dim2[0] - sliceRow, dim2[1]]);
			return tf.concat([sliceParent1, sliceParent2], 0);
		});
	}


}
