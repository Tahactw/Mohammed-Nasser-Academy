import { useState, useCallback } from 'react'
import { usersApi } from '@/services/api/users'
import { useAuth } from '@/context/AuthContext'
import { useNotification } from '@/context/NotificationContext'

export const useBlockUser = () => {
  const { profile } = useAuth()
  const { showNotification } = useNotification()
  const [loading, setLoading] = useState(false)

  const blockUser = useCallback(async (userId: string) => {
    if (!profile) return false

    setLoading(true)
    try {
      await usersApi.blockUser(profile.id, userId)
      showNotification('User blocked', 'success')
      return true
    } catch (error) {
      showNotification('Failed to block user', 'error')
      return false
    } finally {
      setLoading(false)
    }
  }, [profile, showNotification])

  const unblockUser = useCallback(async (userId: string) => {
    if (!profile) return false

    setLoading(true)
    try {
      await usersApi.unblockUser(profile.id, userId)
      showNotification('User unblocked', 'success')
      return true
    } catch (error) {
      showNotification('Failed to unblock user', 'error')
      return false
    } finally {
      setLoading(false)
    }
  }, [profile, showNotification])

  const checkBlocked = useCallback(async (userId: string) => {
    if (!profile) return false

    try {
      return await usersApi.isBlocked(profile.id, userId)
    } catch (error) {
      return false
    }
  }, [profile])

  return {
    blockUser,
    unblockUser,
    checkBlocked,
    loading
  }
}