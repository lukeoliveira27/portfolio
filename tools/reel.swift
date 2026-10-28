// Junta trechos de vídeos (mesma resolução) num showreel, sem áudio.
// Uso: swift reel.swift saida.mp4 arquivo:inicio:duracao ...
import AVFoundation

let args = CommandLine.arguments
let out = URL(fileURLWithPath: args[1])
let comp = AVMutableComposition()
let track = comp.addMutableTrack(withMediaType: .video, preferredTrackID: kCMPersistentTrackID_Invalid)!
var cursor = CMTime.zero
let sem = DispatchSemaphore(value: 0)

for spec in args.dropFirst(2) {
    let p = spec.split(separator: ":").map(String.init)
    let asset = AVURLAsset(url: URL(fileURLWithPath: p[0]))
    let src = asset.tracks(withMediaType: .video)[0]
    let range = CMTimeRange(start: CMTime(seconds: Double(p[1])!, preferredTimescale: 600),
                            duration: CMTime(seconds: Double(p[2])!, preferredTimescale: 600))
    try! track.insertTimeRange(range, of: src, at: cursor)
    cursor = cursor + range.duration
}
try? FileManager.default.removeItem(at: out)
let ex = AVAssetExportSession(asset: comp, presetName: AVAssetExportPreset960x540)!
ex.outputURL = out
ex.outputFileType = .mp4
ex.shouldOptimizeForNetworkUse = true
ex.exportAsynchronously { sem.signal() }
sem.wait()
print(ex.status == .completed ? "ok \(cursor.seconds)s" : "erro: \(String(describing: ex.error))")
