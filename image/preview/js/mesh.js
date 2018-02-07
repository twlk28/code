class DaMesh extends DaObject {
    // 表示三维物体的类
    constructor() {
        super()

        this.position = DaVector.new(0, 0, 0)
        this.rotation = DaVector.new(0, 0, 0)
        this.scale = DaVector.new(1, 1, 1)
        this.vertices = null
        this.indices = null
        this.texture = null
    }
    static fromDa3d(da3dString, textureString){
        let texture = DaImage.fromString(textureString)
        let s = da3dString.split('\n')
        let numberOfVertices = parseInt(s[2].split(' ')[1])
        let numberOfIndices = parseInt(s[3].split(' ')[1])

        let begin = 4 // 第5行开始是顶点数据
        let vertices = []
        for (let i = 0; i < numberOfVertices; i++) {
            let line = s[begin+i].split(' ')
            let [x, y, z, u, v] = [line[0], line[1], line[2], +line[6], +line[7]]
            let vector = DaVector.new(x, y, z)
            let color = DaColor.red()
            vertices[i] = DaVertex.new(vector, u, v, color)
        }

        begin += numberOfVertices
        let indices = []
        for (let j = 0; j < numberOfIndices; j++) {
            let line = s[begin+j].split(' ')
            indices[j] = [line[0], line[1], line[2]]
        }

        let m = this.new()
        m.vertices = vertices
        m.indices = indices
        m.texture = texture
        return m
    }
    // 返回一个正方体
    static cube() {
        // 8 points
        let points = [
            -1, 1,  -1,     // 0
            1,  1,  -1,     // 1
            -1, -1, -1,     // 2
            1,  -1, -1,     // 3
            -1, 1,  1,      // 4
            1,  1,  1,      // 5
            -1, -1, 1,      // 6
            1,  -1, 1,      // 7
        ]

        let vertices = []
        for (let i = 0; i < points.length; i += 3) {
            let v = DaVector.new(points[i], points[i+1], points[i+2])
            let c = DaColor.randomColor()
            vertices.push(DaVertex.new(v, 0, 0, c))
        }

        // 12 triangles * 3 vertices each = 36 vertex indices
        let indices = [
            // 12
            [0, 1, 2],
            [1, 3, 2],
            [1, 7, 3],
            [1, 5, 7],
            [5, 6, 7],
            [5, 4, 6],
            [4, 0, 6],
            [0, 2, 6],
            [0, 4, 5],
            [5, 1, 0],
            [2, 3, 7],
            [2, 7, 6],
        ]
        let m = this.new()
        m.vertices = vertices
        m.indices = indices
        return m
    }
}

class DaImage extends DaObject {
    constructor(dict){
        super()
        if (dict){
            this.width = dict.width
            this.height = dict.height
            this._pixels = dict.pixels
        }
        else {
            this.width = 0
            this.height = 0
            this._pixels = []
        }
    }
    static fromString(daImageString){
        let s = daImageString.split('\n')
        let width = parseInt(s[2])
        let height = parseInt(s[3])
        let pixels = []
        let begin = 4 // 第5行开始是像素值
        for (let i = 0; i < height; i++) {
            let line = s[begin+i] || ''
            let linePixels = line.split(' ')
            for (let j = 0; j < width; j++) {
                let pixel = parseInt(linePixels[j]) || 0
                let [r, g, b, a] = rgbaFromPixel(pixel)
                let color = DaColor.new(r, g, b, a)
                pixels.push(color)
            }
        }
        let image = DaImage.new({width, height, pixels})
        return image
    }
    colorFromUV(u, v){
        // u v 是 0-1的小数, 乘上宽高表示第几个像素
        let int = Math.round
        let x = int(u * this.width)
        let y = int(v * this.height)
        let i = y * this.width + x
        let color = this._pixels[i]
        return color
    }
    colorFromXY(x, y){
        let int = Math.round
        let i = int(y) * this.width + int(x)
        let color = this._pixels[i] || DaColor.red()
        return color
    }
}
