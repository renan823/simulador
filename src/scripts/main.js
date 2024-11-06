/*
Constantes adaptadas para a simulação
*/
const GRAVITY = 0.9;
const VISCOSITY = 0.02; //ta certo isso?
const SCREEN_W = 1000;
const SCREEN_H = 800;

/*
A classe foguete é a responsável por modelar o principal agente do sistema.
O foguete começa parado na posição indicada na sua criação (X e Y).
A velocidade e aceleração inicialmente são nulas.
A massa do foguete é padrão de 500 Kg (devemos considerar massa variável pelo combustível?)

O método #getThrust calcula e retorna o vetor empuxo gerado pelo motor do foguete.
Como representar esse valor? Ele depende da potência? E do combustível?
Por enquanto, apenas um vetor genérico é retornado.

O método #getWeight calcula e retorna a força peso aplicada sobre o foguete.
Essa força é resultante da massa do foguete e da massa do combustível.
Por enquanto, como não estamos trabalhando com combustível, retorna apenas o 
peso calculado com a massa.

O método #getViscosity calcula e retorna a força viscosa aplicada no foguete.
Seu cálculo leva em conta a constante de viscosidade (resistência) do ar e o
vetor velocidade do móvel.
*/
class Rocket {
    constructor(x, y) {
        this.width = 20;
        this.height = 100;
        this.pos = createVector(x, y);
        this.vel = createVector(0, 0);
        this.acc = createVector(0, 0);
        this.mass = 500;
    }

    #getThrust() {
        //Como calcular o empuxo gerado?
        return createVector(0, 800);
    }

    #getWeight() {
        return createVector(0, GRAVITY * this.mass);
    }

    #getViscosity() {
        return createVector(this.vel.x * VISCOSITY, this.vel.y * VISCOSITY);
    }

    #getResultantForce() {
        return createVector(this.#getThrust().x - this.#getViscosity().x, this.#getThrust().y - this.#getWeight().y - this.#getViscosity().y);
    }

    #getAcceleration() {
        const force = this.#getResultantForce();
        return createVector(force.x / this.mass, force.y / this.mass);
    }

    update(dt) {
        this.acc = this.#getAcceleration();
        this.vel.add(p5.Vector.mult(this.acc, dt));
        this.pos.add(p5.Vector.mult(this.vel, dt));
    }
}

//-----------------------------------------------------
let r;

function setup() {
    createCanvas(SCREEN_W, SCREEN_H);

    //define o foguete
    r = new Rocket(SCREEN_W / 2 - 10, SCREEN_H - 150);
}
   
function draw() {
    background("lightblue");
	
    //desenha o foguete na tela 
    rect(r.pos.x, r.pos.y, r.width, r.height);
}