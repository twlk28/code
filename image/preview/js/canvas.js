class DaCamera extends DaObject {
    constructor() {
        super()
        this.position = DaVector.new(0, 0, -10)
        this.target = DaVector.new(0, 0, 0)
        this.up = DaVector.new(0, 1, 0)
    }
}

class DaCanvas extends DaObject {
    constructor(selector) {
        super()
        let canvas = _e(selector)
        this.canvas = canvas
        this.context = canvas.getContext('2d')
        this.w = canvas.width
        this.h = canvas.height
        this.pixels = this.context.getImageData(0, 0, this.w, this.h)
        this.bytesPerPixel = 4
        this.zbuffer = []
        this.camera = DaCamera.new()
    }
    render() {
        let {pixels, context} = this
        context.putImageData(pixels, 0, 0)
    }
    clear(color=DaColor.transparent()) {
        let {w, h} = this
        this.zbuffer = []
        for (let x = 0; x < w; x++) {
            for (let y = 0; y < h; y++) {
                this._setPixel(x, y, Number.MAX_SAFE_INTEGER, color)
            }
        }
        this.zbuffer = []
        this.render()
    }
    _getPixel(x, y) {
        let int = Math.floor
        x = int(x)
        y = int(y)
        let i = (y * this.w + x) * this.bytesPerPixel
        let p = this.pixels.data
        return DaColor.new(p[i], p[i+1], p[i+2], p[i+3])
    }
    _setPixel(x, y, z, color) {
        let int = Math.round
        x = int(x)
        y = int(y)
        let i = (y * this.w + x) * this.bytesPerPixel
        let p = this.pixels.data
        let {r, g, b, a} = color
        if (this.zbuffer[i] && this.zbuffer[i] < z){
            return
        }
        this.zbuffer[i] = z
        p[i] = int(r)
        p[i+1] = int(g)
        p[i+2] = int(b)
        p[i+3] = int(a)
    }
    drawPoint(point, color=DaColor.black()) {
        let {w, h} = this
        let p = point
        if (p.x >= 0 && p.x <= w) {
            if (p.y >= 0 && p.y <= h) {
                this._setPixel(p.x, p.y, p.z, color)
            }
        }
    }
    drawLine(v1, v2, color=DaColor.black()) {
        let [x1, y1, z1, x2, y2, z2] = [v1.x, v1.y, v1.z, v2.x, v2.y, v2.z]
        let dx = x2 - x1
        let dy = y2 - y1
        let dz = z2 - z1

        if(Math.abs(dx) > Math.abs(dy)) {
            let xmin = Math.min(x1, x2)
            let xmax = Math.max(x1, x2)
            for(let x = xmin; x < xmax; x++) {
                let factor = 0
                if (xmin != xmax){
                    factor = (x - xmin) / (xmax - xmin)
                }
                let y = interpolate(y1, y2, factor)
                let z = interpolate(z1, z2, factor)
                if (xmin == x2){
                    y = interpolate(y2, y1, factor)
                    z = interpolate(z2, z1, factor)
                }
                this.drawPoint(DaVector.new(x, y, z), color)
            }
        } else {
            let ymin = Math.min(y1, y2)
            let ymax = Math.max(y1, y2)
            for(let y = ymin; y < ymax; y++) {
                let factor = 0
                if (ymin != ymax){
                    factor = (y - ymin) / (ymax - ymin)
                }
                let x = interpolate(x1, x2, factor)
                let z = interpolate(z1, z2, factor)
                if (ymin == y2){
                    x = interpolate(x2, x1, factor)
                    z = interpolate(z2, z1, factor)
                }
                this.drawPoint(DaVector.new(x, y, z), color)
            }
        }
    }
    drawScanline(v1, v2, texture) {
        let [a, b] = [v1, v2].sort((va, vb) => va.position.x - vb.position.x)
        let [x1, x2, y, z1, z2] = [a.position.x, b.position.x, a.position.y, a.position.z, b.position.z]
        for (let x = x1; x <= x2; x++) {
            let factor = 0
            if (x2 != x1) {
                factor = (x - x1) / (x2 - x1)
            }
            let v = a.interpolate(b, factor)
            let color = texture.colorFromUV(v.u, v.v)
            this.drawPoint(v.position, color)
        }
    }
    drawTriangle(v1, v2, v3, texture) {
        let [a, b, c] = [v1, v2, v3].sort((va, vb) => va.position.y - vb.position.y)
        let middle_factor = 0
        if (c.position.y - a.position.y != 0) {
            middle_factor = (b.position.y - a.position.y) / (c.position.y - a.position.y)
        }
        let middle = a.interpolate(c, middle_factor)
        let start_y = a.position.y
        let end_y = b.position.y
        for (let y = start_y; y <= end_y; y++) {
            let factor = 0
            if (end_y != start_y) {
                factor = (y - start_y) / (end_y - start_y)
            }
            let va = a.interpolate(middle, factor)
            let vb = a.interpolate(b, factor)
            this.drawScanline(va, vb, texture)
        }
        start_y = b.position.y
        end_y = c.position.y
        for (let y = start_y; y <= end_y; y++) {
            let factor = 0
            if (end_y != start_y) {
                factor = (y - start_y) / (end_y - start_y)
            }
            let va = middle.interpolate(c, factor)
            let vb = b.interpolate(c, factor)
            this.drawScanline(va, vb, texture)
        }
    }
    project(coordVector, transformMatrix) {
        let {w, h} = this
        let [w2, h2] = [w/2, h/2]
        let point = transformMatrix.transform(coordVector.position)
        let x = point.x * w2 + w2
        let y = - point.y * h2 + h2
        let z = point.z

        let v = DaVector.new(x, y, z)
        return DaVertex.new(v, coordVector.u, coordVector.v, coordVector.color)
    }
    drawMesh(mesh) {
        let self = this
        // camera
        let {w, h} = this
        let {position, target, up} = self.camera
        const view = Matrix.lookAtLH(position, target, up)
        const projection = Matrix.perspectiveFovLH(0.5, w / h, 0.1, 1)

        const rotation = Matrix.rotation(mesh.rotation)
        const translation = Matrix.translation(mesh.position)

        const world = rotation.multiply(translation)
        const transform = world.multiply(view).multiply(projection)

        for (let t of mesh.indices) {
            let [a, b, c] = t.map(i => mesh.vertices[i])
            let [v1, v2, v3] = [a, b, c].map(v => self.project(v, transform))
            self.drawTriangle(v1, v2, v3, mesh.texture)
        }
    }
    drawImage(daImageString){
        let image = DaImage.fromString(daImageString)
        let {width, height} = image
        let begin = 4 // 第5行开始是像素值
        for (let i = 0; i < height; i++) {
            for (let j = 0; j < width; j++) {
                let color = image.colorFromXY(j, i)
                let point = DaVector.new(j, i, 0)
                this.drawPoint(point, color)
            }
        }
    }
}
