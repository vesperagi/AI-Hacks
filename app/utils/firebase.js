import firebase from "firebase/compat/app";
import "firebase/compat/auth";
import "firebase/compat/firestore";
import "firebase/compat/storage";

const firebaseConfig = {
  apiKey: "AIzaSyDyvoL8N-wQObaeF4EPjUGJpIvN3GumA3o",
  authDomain: "vigama-ai-hacks.firebaseapp.com",
  projectId: "vigama-ai-hacks",
  storageBucket: "vigama-ai-hacks.appspot.com",
  messagingSenderId: "547419632764",
  appId: "1:547419632764:web:9f4a35614f3eb44dc345f9",
  measurementId: "G-CC58JCQN7E",
};

if (!firebase.apps.length) {
  firebase.initializeApp(firebaseConfig);
}

// FIRESTORE EXPORTS
export const firestore = firebase.firestore();

// STORAGE EXPORTS
export const storage = firebase.storage();
