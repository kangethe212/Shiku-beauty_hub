// Firebase Configuration for Shiku Beauty Hub
// This file is used for Firebase client-side features (Authentication, Storage, etc.)

const firebaseConfig = {
  apiKey: "AIzaSyBGJL9q7lCmSxI1JlL4NZ6ZqNehfGYxoaY",
  authDomain: "shiku-beuty-hub.firebaseapp.com",
  projectId: "shiku-beuty-hub",
  storageBucket: "shiku-beuty-hub.firebasestorage.app",
  messagingSenderId: "140804076783",
  appId: "1:140804076783:web:caaac8f29154cebda3571a",
  measurementId: "G-QQZ7R2QPV5"
};

// Initialize Firebase (if Firebase SDK is included)
// Uncomment if you want to use Firebase features in frontend:
/*
import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getStorage } from 'firebase/storage';
import { getFirestore } from 'firebase/firestore';

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const storage = getStorage(app);
export const db = getFirestore(app);
*/

// Or if using script tags:
/*
if (typeof firebase !== 'undefined') {
  firebase.initializeApp(firebaseConfig);
  const auth = firebase.auth();
  const storage = firebase.storage();
  const db = firebase.firestore();
}
*/

