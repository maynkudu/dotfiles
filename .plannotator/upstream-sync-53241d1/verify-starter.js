(() => {
  const game = window.__skimmer;
  const canvas = document.getElementById('c');
  const requireCheck = (condition, message) => {
    if (!condition) throw new Error(message);
  };
  requireCheck(Boolean(game), 'Starter hook is missing');
  requireCheck(canvas.width === 360 && canvas.height === 280, 'Canvas dimensions differ');
  requireCheck(game.G.phase === 'aim' && game.G.left === 5, 'Initial round is inconsistent');
  requireCheck(document.getElementById('mute').getAttribute('aria-pressed') === 'true', 'Sound toggle did not update');
  const shots = [];
  for (const power of [.2, .92, .92, .2, .92]) {
    game.throwAt(power);
    game.step(.13, true);
    requireCheck(Boolean(game.G.stone), 'Release did not launch a stone');
    requireCheck(document.getElementById('status').textContent === 'watch it skip', 'Launch status is stale');
    for (let frame = 0; frame < 600; frame++) game.step(1 / 60, true);
    shots.push({ power, skips: game.G.skips, phase: game.G.phase, left: game.G.left });
  }
  requireCheck(shots[1].skips > shots[0].skips, 'Strong and weak throws have the same outcome');
  requireCheck(game.G.phase === 'over' && game.G.left === 0, 'Five stones did not end the round');
  const total = game.G.total;
  const best = game.G.best;
  requireCheck(total === shots.reduce((sum, shot) => sum + shot.skips, 0), 'Round total differs from the throws');
  requireCheck(Number(localStorage.getItem('iso-pixel:skimmer:best')) === best, 'Best score was not saved');
  game.throwAt(0);
  requireCheck(game.G.phase === 'aim' && game.G.left === 5 && game.G.total === 0 && game.G.skips === 0, 'Round reset is inconsistent');
  requireCheck(game.G.best === best, 'Reset discarded the best score');
  game.step(0);
  const corners = [[0, 0], [359, 0], [0, 279], [359, 279]].map(([horizontal, vertical]) =>
    Array.from(canvas.getContext('2d').getImageData(horizontal, vertical, 1, 1).data));
  requireCheck(corners.every(pixel => pixel.every(channel => channel === 255)), 'Canvas corners are not white');
  const output = document.createElement('canvas');
  output.width = canvas.width * 3;
  output.height = canvas.height * 3;
  const context = output.getContext('2d');
  context.imageSmoothingEnabled = false;
  context.drawImage(canvas, 0, 0, output.width, output.height);
  requireCheck(output.toDataURL().startsWith('data:image/png;base64,'), 'Still export is not a PNG');
  return { shots, total, best, reset: { phase: game.G.phase, left: game.G.left, total: game.G.total },
    canvas: [canvas.width, canvas.height], corners, stillExport: [output.width, output.height] };
})()
