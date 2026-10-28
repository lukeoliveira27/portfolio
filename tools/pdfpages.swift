// Renderiza páginas de um PDF em PNG. Uso: swift pdfpages.swift arquivo.pdf pasta largura pagina1 pagina2 ...
import PDFKit
import AppKit

let a = CommandLine.arguments
let doc = PDFDocument(url: URL(fileURLWithPath: a[1]))!
let dir = a[2]; let width = CGFloat(Double(a[3])!)
for s in a.dropFirst(4) {
    let i = Int(s)! - 1
    guard let page = doc.page(at: i) else { continue }
    let box = page.bounds(for: .mediaBox)
    let scale = width / box.width
    let size = NSSize(width: box.width * scale, height: box.height * scale)
    let img = page.thumbnail(of: size, for: .mediaBox)
    let rep = NSBitmapImageRep(data: img.tiffRepresentation!)!
    try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: "\(dir)/p\(s).png"))
}
print("ok \(doc.pageCount)")
