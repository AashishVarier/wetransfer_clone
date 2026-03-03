import { render, screen } from '@testing-library/react'
import App from '../src/App'

describe('App Component', () => {
  test('renders the main title', () => {
    render(<App />)
    const titleElement = screen.getByText(/WeTransfer Clone/i)
    expect(titleElement).toBeInTheDocument()
  })

  test('renders the upload form section', () => {
    render(<App />)
    const uploadSection = screen.getByText(/Click to select a file/i)
    expect(uploadSection).toBeInTheDocument()
  })

  test('renders the files section', () => {
    render(<App />)
    const filesSection = screen.getByText(/Your Files/i)
    expect(filesSection).toBeInTheDocument()
  })

  // TODO: Add more comprehensive tests
  // TODO: Test file upload functionality
  // TODO: Test file list rendering
  // TODO: Test error handling
})
