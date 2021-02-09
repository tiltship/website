function draw(ctx, startX, startY, len, angle, angleShift, startingWidth, idx=0) {
  ctx.beginPath();
  ctx.save();
  ctx.lineWidth = `${startingWidth*(.9**idx)}`
  ctx.strokeStyle = `rgb(${80 + 10*idx}, 180, ${120 + idx*15}, ${.6*(.65**idx)} )`;
  ctx.translate(startX, startY);
  ctx.rotate(angle * Math.PI/180);
  ctx.moveTo(0, 0);
  ctx.lineTo(0, -len);
  ctx.stroke();

  if (idx === 10) {
    ctx.restore();
    return;
  }

  draw(ctx, 0, -len, len*0.85, -angleShift, angleShift, startingWidth, idx+1);
  draw(ctx, 0, -len, len*0.85, angleShift, angleShift, startingWidth, idx+1);

  ctx.restore();
}

function drawTree(c) {
  c.width = c.clientWidth
  c.height = c.clientHeight

  const l = Math.round(c.clientHeight / 5)
  const as = Math.ceil(c.clientWidth**.6 / 6)
  const sw = Math.ceil(c.clientWidth**.6 / 2)

  draw(c.getContext('2d'), Math.round(c.clientWidth/2), c.clientHeight, l, 0, as, sw)
}

export default drawTree;
