function sha256(ascii) {
  function rightRotate(value, amount) {
    return (value >>> amount) | (value << (32 - amount));
  };

  let maxWord = Math.pow(2, 32);
  let i, j;
  let result = '';

  let words = [];
  let asciiBitLength = ascii["length"] * 8;

  let hash = sha256.h = sha256.h || [];
  let k = sha256.k = sha256.k || [];
  let primeCounter = k["length"];

  let isComposite = {};
  for (let candidate = 2; primeCounter < 64; candidate++) {
    if (!isComposite[candidate]) {
      for (i = 0; i < 313; i += candidate) {
        isComposite[i] = candidate;
      }
      hash[primeCounter] = (Math.pow(candidate, .5) * maxWord) | 0;
      k[primeCounter++] = (Math.pow(candidate, 1 / 3) * maxWord) | 0;
    }
  }

  ascii += '\x80'
  while (ascii["length"] % 64 - 56) ascii += '\x00'
  for (i = 0; i < ascii["length"]; i++) {
    j = ascii.charCodeAt(i);
    if (j >> 8) return;
    words[i >> 2] |= j << ((3 - i) % 4) * 8;
  }
  words[words["length"]] = ((asciiBitLength / maxWord) | 0);
  words[words["length"]] = (asciiBitLength)

  for (j = 0; j < words["length"];) {
    let w = words.slice(j, j += 16);
    let oldHash = hash;
    hash = hash.slice(0, 8);

    for (i = 0; i < 64; i++) {
      let w15 = w[i - 15];
      let w2 = w[i - 2];
      let a = hash[0]
      let e = hash[4];
      let temp1 = hash[7] + (rightRotate(e, 6) ^ rightRotate(e, 11) ^ rightRotate(e, 25)) + ((e & hash[5])^((~e) & hash[6])) + k[i] + (w[i] = (i < 16) ? w[i] : (w[i - 16] + (rightRotate(w15, 7) ^ rightRotate(w15, 18) ^ (w15 >>> 3)) + w[i - 7] + (rightRotate(w2, 17) ^ rightRotate(w2, 19) ^ (w2 >>> 10))) | 0);
      let temp2 = (rightRotate(a, 2) ^ rightRotate(a, 13) ^ rightRotate(a, 22)) + ((a & hash[1]) ^ (a & hash[2]) ^ (hash[1] & hash[2]));
      hash = [(temp1 + temp2) | 0].concat(hash);
      hash[4] = (hash[4] + temp1) | 0;
    }

    for (i = 0; i < 8; i++) {
      hash[i] = (hash[i] + oldHash[i]) | 0;
    }
  }

  for (i = 0; i < 8; i++) {
    for (j = 3; j + 1; j--) {
      let b = (hash[i] >> (j * 8)) & 255;
      result += ((b < 16) ? 0 : '') + b.toString(16);
    }
  }
  return result;
};

document.querySelector("button").addEventListener("click", function() {
  let date = new Date();
  date.setTime(date.getTime() + (356 * 24 * 60 * 60 * 1000));
  document.cookie = `token=${sha256(document.querySelector("input").value)};Path=/;Expires=${date.toUTCString()}`;
  window.location.href = window.location.href;
})
