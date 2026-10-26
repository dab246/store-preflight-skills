import SwiftUI
import GoogleSignIn
import CoreLocation
import StripePaymentSheet

final class SessionStore: ObservableObject {
    private let locationManager = CLLocationManager()
    private let defaults = UserDefaults.standard

    var isTestFlight: Bool {
        Bundle.main.appStoreReceiptURL?.lastPathComponent == "sandboxReceipt"
    }

    func signInWithGoogle() {
        GIDSignIn.sharedInstance.signIn(withPresenting: rootViewController)
    }

    func registerForPush() {
        UIApplication.shared.registerForRemoteNotifications()
    }
}
