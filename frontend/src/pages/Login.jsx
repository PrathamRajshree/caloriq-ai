import { useState } from "react"
import { auth } from "../services/firebase"
import {
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
} from "firebase/auth"

export default function Login() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")

  const handleAuth = async () => {
    setError("")
    try {
      await signInWithEmailAndPassword(auth, email, password)
    } catch {
      try {
        await createUserWithEmailAndPassword(auth, email, password)
      } catch (err) {
        setError(err.message)
      }
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-xl shadow w-80">
        <h1 className="text-2xl font-bold text-center mb-4">
          Caloriq
        </h1>

        <input
          type="email"
          placeholder="Email"
          className="w-full p-2 mb-3 border rounded"
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          className="w-full p-2 mb-3 border rounded"
          onChange={(e) => setPassword(e.target.value)}
        />

        {error && (
          <p className="text-red-500 text-sm mb-2">
            {error}
          </p>
        )}

        <button
          onClick={handleAuth}
          className="w-full bg-green-500 text-white py-2 rounded hover:bg-green-600"
        >
          Login / Signup
        </button>
      </div>
    </div>
  )
}
