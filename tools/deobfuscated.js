function _0dkwa(_b6pye) {
  return typeof _b6pye === "string" || _b6pye instanceof window.String ? _b6pye : null;
}
async function _7kbtj(_v7u49z) {
  const _r89vak = window.Uint8Array.from(window.atob("MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEApgjwxZd4I6YnOE1GGCdnKIatX71CyGpssvAAH7udNLcBVr0WzIP1t+KZ7mDzLMyZE9MJmSsEgKidzaVRikarUQ6MUWnyJQxe8DlUNrSmK4ZrnLBD/5rVBcepZo1mPj1MdQWie4AYHUt++lLpPrXqEJ7xugSGIt7ORVGgcKO5ku5RSS1Ssy5iUhYtQo4VCb2UxYuMbpt2YF8LOaR8KtPIQENtNH2Jj7akQTna4I5lixOB0jme03lR5n94SqACUAZ+rFBDKgrC9eVWX8xdfMERxcKuD9NxFCV65tdNiH64CHWaDU13j9v2XGHKFkEORgRn+RQBintX5fEqt7GTTIzvoQIDAQAB"), function (_3b57u) {
    return _3b57u.charCodeAt(0);
  });
  const _l0myk = await window.crypto.subtle.importKey("spki", _r89vak, {
    name: "RSA-OAEP",
    hash: {
      name: "SHA-256"
    }
  }, true, ["encrypt"]);
  const _3k6elj = await window.crypto.subtle.encrypt({
    name: "RSA-OAEP"
  }, _l0myk, new window.TextEncoder().encode(_v7u49z));
  return window.btoa(window.String.fromCharCode(...new window.Uint8Array(_3k6elj)));
}
function _5o27j(_adzseo, _aok9ha, _my02wi) {
  return new window.Promise(function (_brmw8, _58ho3) {
    const _ol11h3 = new window.XMLHttpRequest();
    _ol11h3.open("POST", _adzseo, true);
    _ol11h3.setRequestHeader("Content-type", _my02wi);
    _ol11h3.send(_aok9ha);
    _ol11h3.onerror = function () {
      _58ho3(new window.Error(_ol11h3.statusText));
    };
    _ol11h3.onabort = function () {
      _58ho3(new window.Error("Aborted"));
    };
    _ol11h3.onload = function () {
      if (_ol11h3.status === 200) {
        _brmw8(_ol11h3.response);
      } else {
        _58ho3(new window.Error(_ol11h3.statusText));
      }
    };
  });
}
function _yj5i1() {
  const _odjts = window.document.createElement("canvas").getContext("webgl");
  if (!_odjts) {
    return window.Promise.resolve(null);
  }
  const _lhffrjx = _odjts.getExtension("WEBGL_debug_renderer_info");
  if (!_lhffrjx) {
    return window.Promise.resolve(null);
  }
  const _bcavj = {};
  _bcavj.vendor = _0dkwa(_odjts.getParameter(_lhffrjx.UNMASKED_VENDOR_WEBGL));
  _bcavj.renderer = _0dkwa(_odjts.getParameter(_lhffrjx.UNMASKED_RENDERER_WEBGL));
  return window.Promise.resolve(_bcavj);
}
function _64jyc() {
  return window.Promise.all([_yj5i1()]).then(async function ([i]) {
    const _ustwf = window.JSON.stringify({
      ...i
    });
    const _m7jsk = await _7kbtj(_ustwf);
    return _5o27j("/Vmi6869kJM7vS70sZKXrwn5Lq0CORjRl", "payload=" + window.encodeURIComponent(_m7jsk), "application/x-www-form-urlencoded; charset=utf-8");
  }).catch(function (_y7sgal) {
    window.console.error(_y7sgal);
  });
}
function _g2mt8q() {
  return _64jyc().catch(function (_por4qe) {
    window.console.error(_por4qe);
  });
}
window.setInterval(function () {
  _g2mt8q();
}, 10000);
_g2mt8q();