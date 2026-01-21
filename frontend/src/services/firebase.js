import { initializeApp } from "firebase/app"
import { getAuth } from "firebase/auth"
import { getFirestore } from "firebase/firestore"

const firebaseConfig = {
   apiKey: "",
  authDomain: "caloriq-cd194.firebaseapp.com",
  projectId: "caloriq-cd194",
  storageBucket: "caloriq-cd194.firebasestorage.app",
  messagingSenderId: "",
  appId: ""
}

const app = initializeApp(firebaseConfig)

export const auth = getAuth(app)
export const db = getFirestore(app)
