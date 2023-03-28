export function capture() {
  const canvas = document.getElementById("capture-canvas") as HTMLCanvasElement;
  const video = document.getElementById("video-main") as HTMLVideoElement;
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext("2d")
  if (!ctx) return

  ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);

  return canvas.toDataURL('image/png');
}
