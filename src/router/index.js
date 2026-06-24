import { createRouter, createWebHistory } from 'vue-router'
import LogoutView from '../views/LogoutView.vue'
import LandingPageView from '../views/LandingPageView.vue'
import LoginPageView from '../views/LoginPageView.vue'
import SignUpView from '../views/SignUpView.vue'
import AboutUsView from '../views/AboutUsView.vue'
import SearchFlightsPageView from '../views/SearchFlightsPageView.vue'
import SearchFlightsResultsView from '../views/SearchFlightsResultsView.vue'
import PaymentGateawayView from '../views/PaymentGateawayView.vue'
import FlightInfoView from '../views/FlightInfoView.vue'
import FlightPackageView from '../views/FlightPackageView.vue'
import ProfileView from '../views/ProfileView.vue'
import CountryInfoView from '../views/CountryInfoView.vue'
import FlightBookingView from '../views/FlightBookingView.vue'
import SettingsView from '../views/SettingsView.vue'
import ShuttleServiceView from '../views/ShuttleServiceView.vue'
import FlightBookingConfirmationView from '../views/FlightBookingConfirmationView.vue'
import FlightDetailsView from '../views/FlightDetailsView.vue'
import WeatherInfoView from '../views/WeatherInfoView.vue'
import LoyatyPointsView from '@/views/LoyatyPointsView.vue'
import MyBookingsView from '@/views/MyBookingsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Landing',
      component: LandingPageView,
    },
    {
      path: '/aboutus',
      name: 'about',
      component: AboutUsView,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginPageView,
    },
    {
      path: '/logout',
      name: 'logout',
      component: LogoutView,
    },
    {
      path: '/flight-search',
      name: 'flightSearch',
      component: SearchFlightsPageView,
    },
    {
      path: '/flight-search/results',
      name: 'flightResults',
      component: SearchFlightsResultsView,
    },
    {
      path: '/flight-search/results/flight/:flightId',
      name: 'flightDetails',
      component: FlightDetailsView,
    },
    {
      path: '/book-flight/payment',
      name: 'flightPayment',
      component: PaymentGateawayView,
    },
    {
      path: '/book-flight',
      name: 'flightBooking',
      component: FlightBookingView,
    },
    {
      path: '/book-flight/confirmation',
      name: 'flightBookingConfirmation',
      component: FlightBookingConfirmationView,
    },
    {
      path: '/flight-info',
      name: 'flightInfo',
      component: FlightInfoView,
    },
    {
      path: '/flight-packages',
      name: 'packageandDeals',
      component: FlightPackageView,
    },
    {
      path: '/profile',
      name: 'userProfile',
      component: ProfileView,
    },
    {
      path: '/profile/my-bookings',
      name: 'Bookings',
      component: MyBookingsView,
    },
    {
      path: '/profile/loyalty-points',
      name: 'loyaltyPoints',
      component: LoyatyPointsView,
    },
    {
      path: '/profile/settings',
      name: 'Settings',
      component: SettingsView,
    },
    {
      path: '/country-info',
      name: 'countryInfo',
      component: CountryInfoView,
    },
    {
      path: '/shuttle-service',
      name: 'shuttleService',
      component: ShuttleServiceView,
    },
    {
      path: '/weather-info',
      name: 'weatherInfo',
      component: WeatherInfoView,
    },
  ],
})

export default router
