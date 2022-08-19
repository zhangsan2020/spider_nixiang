
const CryptoJS = require("D:\\live\\all_study_new\\spider\\node_modules\\crypto-js")
// const CryptoJS = require("crypto-js");
// import CryptoJS from "crypto-js";

CryptoJS.mode.ECB = (function() {
  var ECB = CryptoJS.lib.BlockCipherMode.extend();
  ECB.Encryptor = ECB.extend({
    processBlock: function(words, offset) {
      this._cipher.encryptBlock(words, offset);
    },
  });

  ECB.Decryptor = ECB.extend({
    processBlock: function(words, offset) {
      this._cipher.decryptBlock(words, offset);
    },
  });
  return ECB;
})();
//DES 加密
function encryptByDES(message) {
  var keyHex = CryptoJS.enc.Utf8.parse("ctpstp@custominfo!@#qweASD");
  var encrypted = CryptoJS.DES.encrypt(message, keyHex, {
    mode: CryptoJS.mode.ECB,
    padding: CryptoJS.pad.Pkcs7,
  });
  return encrypted.toString();
}
//DES 解密
function decryptByDES(ciphertext) {
  var keyHex = CryptoJS.enc.Utf8.parse("ctpstp@custominfo!@#qweASD");
  // direct decrypt ciphertext
  var decrypted = CryptoJS.DES.decrypt(
    {
      ciphertext: CryptoJS.enc.Base64.parse(ciphertext),
    },
    keyHex,
    {
      mode: CryptoJS.mode.ECB,
      padding: CryptoJS.pad.Pkcs7,
    }
  );
  return decrypted.toString(CryptoJS.enc.Utf8);
}

// name = 'zhanglei';
// console.log(encryptByDES(name));