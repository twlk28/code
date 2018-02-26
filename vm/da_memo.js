class DaMemo extends DaObject {
    constructor(){
        super()
        this.size = 2**16
        this.data = new Array(this.size).fill(0)
    }
    writeAtIndex(atIndex, data) {
        if (Array.isArray(data)){
            data.forEach((e, i)=>{
                this.data[atIndex+i] = e
            })
        }
        else {
            this.data[atIndex] = data
        }
    }
    readAtIndex(atIndex){
        return this.data[atIndex]
    }
}
DaMemo.wordSize = 2
