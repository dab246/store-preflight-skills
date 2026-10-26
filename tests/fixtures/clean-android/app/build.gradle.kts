plugins { id("com.android.application") }

android {
    namespace = "io.github.dab246.notes"
    compileSdk = 36
    defaultConfig {
        applicationId = "io.github.dab246.notes"
        minSdk = 26
        targetSdk = 36
    }
}

dependencies {
    implementation("com.android.billingclient:billing-ktx:8.0.0")
}
