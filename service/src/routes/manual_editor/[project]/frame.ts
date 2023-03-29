export function capture() {
  const canvas = document.getElementById("capture-canvas") as HTMLCanvasElement;
  const video = document.getElementById("video-main") as HTMLVideoElement;
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext("2d")
  if (!ctx) return

  ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);

  // const img = new Image()
  // img.onload = (event) => {
  //   img.src = "path to image asset";
  // img.onload = () => {
  //   const startX = video.videoWidth / 2 - img.width / 2;
  //   const startY = video.videoHeight / 2 - img.height / 2;
  //   ctx.drawImage(img, startX, startY, img.width, img.height);
  //   canvas.toBlob() = (blob) => {
  //     const img = new Image();
  //     img.src = window.URL.createObjectUrl(blob);
  //   };
  //
  // }
  return canvas.toDataURL('image/png');
}
