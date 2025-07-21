import axios from 'axios'
import { TransactionItem } from '@/types'

const PAYMOB_API_URL = 'https://accept.paymob.com/api'
const PAYMOB_API_KEY = import.meta.env.VITE_PAYMOB_API_KEY
const PAYMOB_IFRAME_ID = import.meta.env.VITE_PAYMOB_IFRAME_ID

interface PaymobAuthResponse {
  token: string
}

interface PaymobOrderResponse {
  id: number
}

interface PaymobPaymentKeyResponse {
  token: string
}

export class PaymobService {
  private apiKey: string
  private iframeId: string

  constructor() {
    this.apiKey = PAYMOB_API_KEY
    this.iframeId = PAYMOB_IFRAME_ID

    if (!this.apiKey || !this.iframeId) {
      throw new Error('Paymob configuration missing')
    }
  }

  // Step 1: Authentication
  private async authenticate(): Promise<string> {
    try {
      const response = await axios.post<PaymobAuthResponse>(
        `${PAYMOB_API_URL}/auth/tokens`,
        {
          api_key: this.apiKey
        }
      )
      return response.data.token
    } catch (error) {
      console.error('Paymob authentication failed:', error)
      throw new Error('Payment authentication failed')
    }
  }

  // Step 2: Create order
  private async createOrder(
    authToken: string,
    amount: number,
    items: TransactionItem[]
  ): Promise<number> {
    try {
      const response = await axios.post<PaymobOrderResponse>(
        `${PAYMOB_API_URL}/ecommerce/orders`,
        {
          auth_token: authToken,
          delivery_needed: false,
          amount_cents: Math.round(amount * 100), // Convert to cents
          currency: 'USD',
          items: items.map(item => ({
            name: item.book_id,
            amount_cents: Math.round(item.price * 100),
            quantity: item.quantity
          }))
        }
      )
      return response.data.id
    } catch (error) {
      console.error('Paymob order creation failed:', error)
      throw new Error('Order creation failed')
    }
  }

  // Step 3: Get payment key
  private async getPaymentKey(
    authToken: string,
    orderId: number,
    amount: number,
    billingData: any
  ): Promise<string> {
    try {
      const response = await axios.post<PaymobPaymentKeyResponse>(
        `${PAYMOB_API_URL}/acceptance/payment_keys`,
        {
          auth_token: authToken,
          amount_cents: Math.round(amount * 100),
          expiration: 600, // 10 minutes
          order_id: orderId,
          billing_data: billingData,
          currency: 'USD',
          integration_id: this.iframeId
        }
      )
      return response.data.token
    } catch (error) {
      console.error('Paymob payment key generation failed:', error)
      throw new Error('Payment key generation failed')
    }
  }

  // Main checkout function
  async initiateCheckout(
    amount: number,
    items: TransactionItem[],
    userEmail: string,
    userId: string
  ): Promise<string> {
    try {
      // Step 1: Authenticate
      const authToken = await this.authenticate()

      // Step 2: Create order
      const orderId = await this.createOrder(authToken, amount, items)

      // Step 3: Get payment key
      const billingData = {
        email: userEmail,
        first_name: 'User',
        last_name: userId,
        phone_number: '+201234567890', // Required by Paymob
        country: 'US',
        city: 'N/A',
        street: 'N/A',
        building: 'N/A',
        floor: 'N/A',
        apartment: 'N/A'
      }

      const paymentKey = await this.getPaymentKey(
        authToken,
        orderId,
        amount,
        billingData
      )

      // Return iframe URL
      return `https://accept.paymob.com/api/acceptance/iframes/${this.iframeId}?payment_token=${paymentKey}`
    } catch (error) {
      console.error('Checkout initiation failed:', error)
      throw error
    }
  }

  // Verify transaction (for webhook)
  async verifyTransaction(transactionId: string): Promise<boolean> {
    try {
      const authToken = await this.authenticate()
      
      const response = await axios.get(
        `${PAYMOB_API_URL}/acceptance/transactions/${transactionId}`,
        {
          headers: {
            Authorization: `Bearer ${authToken}`
          }
        }
      )

      return response.data.success === true
    } catch (error) {
      console.error('Transaction verification failed:', error)
      return false
    }
  }

  // Calculate HMAC for webhook verification
  calculateHMAC(data: any, secret: string): string {
    // Implementation depends on Paymob's specific HMAC calculation
    // This is a placeholder - implement according to Paymob docs
    const crypto = require('crypto')
    const hmac = crypto.createHmac('sha512', secret)
    hmac.update(JSON.stringify(data))
    return hmac.digest('hex')
  }
}

export const paymobService = new PaymobService()