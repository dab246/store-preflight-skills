package com.example.demo

class AuthRepository(private val auth: FirebaseAuth, private val http: HttpClient) {
    suspend fun register(email: String, password: String) =
        auth.createUserWithEmailAndPassword(email, password)

    suspend fun summarize(text: String) =
        http.post("https://llm.internal.example/v1/chat/completions", body = text)
}
