export async function getPCM2(blob, audioCtx) {
  const arrayBuffer = await new Response(blob).arrayBuffer();
  const audioBuffer = await audioCtx.decodeAudioData(arrayBuffer);
  const analyser = audioCtx.createAnalyser();

  const source = audioCtx.createBufferSource();

  source.buffer = audioBuffer;
  source.connect(analyser);
}

// @ts-ignore
export async function getPCM(blob, audioCtx, fileReader): Promise<Float32Array> {
  return new Promise((resolve, reject) => {
    fileReader.onloadend = () => {
      if (fileReader.result?.byteLength === 0) return
      const arrayBuffer = fileReader.result as ArrayBuffer;
      // Convert array buffer into audio buffer
      audioCtx.decodeAudioData(arrayBuffer, (audioBuffer) => {
        // Do something with audioBuffer
        const pcm = audioBuffer.getChannelData(0);
        resolve(pcm);
      });
    };
    fileReader.onerror = reject;
    fileReader.readAsArrayBuffer(blob);
  });
}


export function drawPCM(values, canvas, playhead) {
  const ctx = canvas.getContext('2d');
  let { width: clientWidth, height: clientHeight } = canvas;
  canvas.width = clientWidth;
  const scale = 2;
  ctx.scale(scale, scale);
  clientWidth /= scale; // scale down for pretty canvas
  clientHeight /= scale;
  const absoluteValues = true; // if false, we will retain the true waveform
  const valuesPerPixel = values.length / clientWidth;
  const blockSize = 1; // width of one sample block
  let max = 0;
  const averageValues = [];
  for (let x = 0; x < clientWidth; x += blockSize) {
    const area = values.slice(Math.floor(x * valuesPerPixel), Math.ceil((x + blockSize) * valuesPerPixel));
    const areaReducer = absoluteValues ? (sum, v) => sum + Math.abs(v) : (sum, v) => sum + v;
    const value = area.reduce(areaReducer, 0) / area.length;
    max = max < value ? value : max;
    averageValues.push(value);
  }
  averageValues.forEach((value, index) => {
    const height = (((value / max) * clientHeight) / 2) * 0.9;
    ctx.beginPath();
    ctx.strokeStyle = `#3535C3`;
    ctx.fillStyle = `#6464D8`;
    const args = [index * blockSize, clientHeight / 2 - (absoluteValues ? height / 2 : 0), blockSize, height];
    const borderRadius = Math.floor(Math.min(args[2], args[3]) / 2);
    ctx.fillRect(index * blockSize, clientHeight / 2 - (absoluteValues ? height / 2 : 0), blockSize, height);
    ctx.stroke();
  });
  if (playhead) {
    ctx.beginPath();
    const x = playhead * clientWidth;
    ctx.moveTo(x, 0);
    ctx.lineTo(x, clientHeight);
    ctx.stroke();
  }
}
