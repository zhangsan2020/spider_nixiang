// import CryptoJS from "crypto-js";
//
// const key = CryptoJS.enc.Utf8.parse("1234123412ABCDEF");
// const options = {
//   iv: CryptoJS.enc.Utf8.parse("ABCDEF1234123412"),
//   mode: CryptoJS.mode.CBC,
//   padding: CryptoJS.pad.Pkcs7,
// };
//
// //加密方法
// export const Encrypt = (word: any) => {
//   let srcs = CryptoJS.enc.Utf8.parse(word);
//   let encrypted = CryptoJS.AES.encrypt(srcs, key, options);
//   return encrypted.ciphertext.toString().toUpperCase();
// };
//
// //解密方法
// export const Decrypt = (word: any) => {
//   let encryptedHexStr = CryptoJS.enc.Hex.parse(word);
//   let srcs = CryptoJS.enc.Base64.stringify(encryptedHexStr);
//   let decrypt = CryptoJS.AES.decrypt(srcs, key, options);
//   let decryptedStr = decrypt.toString(CryptoJS.enc.Utf8);
//   return decryptedStr.toString();
// };
//
