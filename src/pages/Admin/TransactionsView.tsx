import React, { useState, useEffect } from 'react'
import {
  Box,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  List,
  ListItem,
  ListItemText
} from '@mui/material'
import { Visibility } from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { Transaction } from '@/types'
import { supabase } from '@/services/supabase'

const TransactionsView: React.FC = () => {
  const { t } = useTranslation()
  const [transactions, setTransactions] = useState<Transaction[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedTransaction, setSelectedTransaction] = useState<Transaction | null>(null)
  const [detailsOpen, setDetailsOpen] = useState(false)

  useEffect(() => {
    fetchTransactions()
  }, [])

  const fetchTransactions = async () => {
    try {
      const { data, error } = await supabase
        .from('transactions')
        .select(`
          *,
          user:users(id, username, email)
        `)
        .order('created_at', { ascending: false })

      if (error) throw error
      setTransactions(data || [])
    } catch (error) {
      console.error('Error fetching transactions:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleViewDetails = (transaction: Transaction) => {
    setSelectedTransaction(transaction)
    setDetailsOpen(true)
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'success'
      case 'pending':
        return 'warning'
      case 'failed':
        return 'error'
      default:
        return 'default'
    }
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {t('transactions')}
      </Typography>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>User</TableCell>
              <TableCell>Amount</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Date</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {transactions.map((transaction) => (
              <TableRow key={transaction.id}>
                <TableCell>{transaction.id.substring(0, 8)}...</TableCell>
                <TableCell>{transaction.user?.username}</TableCell>
                <TableCell>${transaction.amount.toFixed(2)}</TableCell>
                <TableCell>
                  <Chip
                    label={transaction.status}
                    color={getStatusColor(transaction.status)}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  {new Date(transaction.created_at).toLocaleDateString()}
                </TableCell>
                <TableCell align="right">
                  <IconButton onClick={() => handleViewDetails(transaction)}>
                    <Visibility />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog
        open={detailsOpen}
        onClose={() => setDetailsOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Transaction Details</DialogTitle>
        <DialogContent>
          {selectedTransaction && (
            <Box>
              <Typography variant="subtitle2" gutterBottom>
                Transaction ID: {selectedTransaction.id}
              </Typography>
              <Typography variant="subtitle2" gutterBottom>
                User: {selectedTransaction.user?.username} ({selectedTransaction.user?.email})
              </Typography>
              <Typography variant="subtitle2" gutterBottom>
                Amount: ${selectedTransaction.amount.toFixed(2)} {selectedTransaction.currency}
              </Typography>
              <Typography variant="subtitle2" gutterBottom>
                Status: <Chip
                  label={selectedTransaction.status}
                  color={getStatusColor(selectedTransaction.status)}
                  size="small"
                />
              </Typography>
              {selectedTransaction.paymob_transaction_id && (
                <Typography variant="subtitle2" gutterBottom>
                  Paymob ID: {selectedTransaction.paymob_transaction_id}
                </Typography>
              )}
              <Typography variant="subtitle2" gutterBottom>
                Created: {new Date(selectedTransaction.created_at).toLocaleString()}
              </Typography>
              {selectedTransaction.completed_at && (
                <Typography variant="subtitle2" gutterBottom>
                  Completed: {new Date(selectedTransaction.completed_at).toLocaleString()}
                </Typography>
              )}
              
              <Typography variant="h6" sx={{ mt: 2 }}>
                Items:
              </Typography>
              <List>
                {selectedTransaction.items?.map((item, index) => (
                  <ListItem key={index}>
                    <ListItemText
                      primary={`Book ID: ${item.book_id}`}
                      secondary={
                        <>
                          Quantity: {item.quantity} × ${item.price} = ${(item.quantity * item.price).toFixed(2)}
                          {item.is_gift && ` (Gift to ${item.recipient_id})`}
                        </>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            </Box>
          )}
        </DialogContent>
      </Dialog>
    </Box>
  )
}

export default TransactionsView