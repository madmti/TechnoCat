// CLASES PRINCIPALES
class HitBox{
    constructor( x, y, size, vel, canvas, img ){
        this.img = img;
        this.pos = {x,y};
        this.size = (size / 100) * canvas.width;
        this.vel = vel;
        this.canvas = canvas;
    };
    draw(ctx){
        ctx.drawImage(
            this.img,
            0,0,
            this.img.width,
            this.img.height,
            this.pos.x,this.pos.y,
            this.size,
            this.size,
        );
    };
    update( Player, OBJ ){
        this.pos.y += this.vel;
        const condx = ( this.pos.x < Player.pos.x && Player.pos.x < this.pos.x + this.size ) || ( this.pos.x < Player.pos.x + Player.size && Player.pos.x + Player.size < this.pos.x + this.size );
        const condy = ( Player.pos.y < this.pos.y && this.pos.y < Player.pos.y + Player.size || Player.pos.y < this.pos.y + this.size && this.pos.y + this.size < Player.pos.y + Player.size );
        condx && condy ? Player.die() : 0;
        
        this.pos.y > this.canvas.height
            ?OBJ.splice(OBJ.indexOf(this), 1)
            :0;
    };
}

class Player{
    constructor( canvas, size, MaxSize, img ){
        this.img = img;
        this.canvas = canvas;
        this.size = canvas.width * size / 100;
        this.size < MaxSize ? 0: this.size = MaxSize;
        this.pos = {
            x: Math.floor( (canvas.width - this.size) / 2 ),
            y: Math.floor( canvas.height - this.size ),
        };
        this.vel = canvas.width / 100;
        this.alive = true;
    };
    draw(ctx){
        ctx.drawImage(
            this.img,
            0,0,
            this.img.width,
            this.img.height,
            this.pos.x - 2.5,this.pos.y - 2.5,
            this.size + 5,
            this.size + 5,
        );
    };
    update(){
        (0 < this.pos.x && this.vel < 0) || (this.pos.x < this.canvas.width - this.size && this.vel > 0)
            ? this.pos.x += this.vel
            : 0;
    };
    die(){
        this.vel = 0;
        this.alive = false;
    };
    toggle(){
        this.vel *= -1;
    };
}

class Generador{
    constructor( canvas, img, lim ){
        this.canvas = canvas;
        this.timer = 0;
        this.img = img;
        this.lastTime = 0;
        this.limit = lim;
        this.RealTime = Math.floor(this.lastTime);
        this.tipes = [
            {
                size:5,
                vel:15
            },
            {
                size:10,
                vel:5
            },
            {
                size:2,
                vel:10
            },
        ]
        this.OBJS = [];
        this.generar();
    }
    addTime( currentTime ){
        const delta = currentTime - this.lastTime;
        this.lastTime = currentTime;
        this.RealTime = Math.floor(currentTime);
        this.timer >= this.limit * 100? this.generar(): this.timer += delta;
    }
    generar(){
        this.timer = 0;
        this.limit -= this.limit <= 10 ? 0 : 1;
        const random = Math.floor(Math.random() * (this.tipes.length));
        this.OBJS.push( HitBoxfromJSON( this.tipes[random < this.tipes.length? random: this.tipes.length - 1], this.canvas, this.img ) );
    }

}

const HitBoxfromJSON = (data, canvas, img) => {
    return new HitBox( Math.floor( Math.random() * (canvas.width - data.size) ), -data.size, data.size, data.vel, canvas, img );
};

// CONSTANTES Y CONFIG
const canvas = document.querySelector('canvas');
canvas.height = canvas.clientHeight;
canvas.width = canvas.clientWidth;
const ctx = canvas.getContext('2d');
const bg = document.querySelector('img#bg');
const pet = document.querySelector('img#pet');
const trash = document.querySelector('img#trash');
const timeSmall = document.querySelector('p.time small');
const caSmall = document.querySelector('p.score small');
const inputCa = document.querySelector('input#CA');
const inputTime = document.querySelector('input#Time');
const formOver = document.querySelector('div.top form');
const timeCA = {
    delta:0,
    last:0,
    real:0,
    timer:0,
    ca:0,
    onGame:true
};
const AllowKeys = ['h', ' '];
const MaxSize = 100;
const RelSize = 10;
const HurtBox = new Player( canvas, RelSize, MaxSize, pet );

const Generadores = [
    new Generador( canvas, trash, 30 ),
    new Generador( canvas, trash, 50 ),
];

// GENERAL DRAW
const clear = () => {
    ctx.drawImage( 
        bg, 
        0, 0, 
        bg.width, 
        bg.height, 
        0, 0, 
        canvas.width, 
        canvas.height );
};

const draw = () => {
    HurtBox.draw(ctx);
    Generadores.forEach((gene) => { gene.OBJS.forEach((el) => { el.draw(ctx) }) });
};

const update = () => {
    HurtBox.update();
    Generadores.forEach((gene) => { gene.OBJS.forEach((el) => { el.update( HurtBox, gene.OBJS ) }) });
};

const timeManager = (time) => {
    timeCA.delta = time - timeCA.last;
    timeCA.last = time;
    timeCA.real = Math.floor(time);
    if(timeCA.timer >= 5000){ timeCA.ca += 1; timeCA.timer = 0 } else {timeCA.timer += timeCA.delta};
    caSmall.innerHTML = timeCA.ca;
    timeSmall.innerHTML = Math.floor(timeCA.real / 1000);
}

const gameOver = () => {
    formOver.style.display = "flex";
    setTimeout(() => { timeCA.onGame = false; }, 500);
};

// MAIN LOOP
const GameLoop = ( time = 0 ) => {
    HurtBox.alive ?timeManager(time):gameOver();
    Generadores.forEach((gene) => { gene.addTime(time) });
    clear();
    draw();
    update();
    timeCA.onGame
        ?requestAnimationFrame( GameLoop ):0;
};
const dontTryToHACKTHEGAME = () => {
    inputCa.value = timeCA.ca;
    inputTime.value = Math.floor(timeCA.real / 1000);
    requestAnimationFrame( dontTryToHACKTHEGAME );
};

// CONTROLES
document.addEventListener('keydown',(e) => {
    AllowKeys.includes(e.key)?HurtBox.toggle():0;
});
document.addEventListener('click', () => {
    HurtBox.toggle();
});

GameLoop();
dontTryToHACKTHEGAME();