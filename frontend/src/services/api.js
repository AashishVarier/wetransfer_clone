// TODO: Replace with actual backend URL from environment
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3000/api'

/**
 * Upload a file to the backend
 * TODO: Implement actual file upload with FormData
 */
export const uploadFile = async (file) => {
  console.log('uploadFile called with:', file)
  
  // TODO: Validate file size (2MB limit)
  // TODO: Create FormData and send to backend
  // TODO: Handle authentication token
  
  return new Promise((resolve) => {
    // Placeholder: simulate async operation
    setTimeout(() => {
      resolve({ success: true, fileId: 'file_' + Date.now() })
    }, 1000)
  })
}

/**
 * Fetch list of uploaded files
 * TODO: Implement actual API call to fetch user's files
 */
export const listFiles = async () => {
  console.log('listFiles called')
  
  // TODO: Call GET /files endpoint
  // TODO: Handle authentication
  // TODO: Parse response and return files
  
  return new Promise((resolve) => {
    // Placeholder: simulate async operation
    setTimeout(() => {
      resolve([])
    }, 500)
  })
}

/**
 * Download a file by ID
 * TODO: Implement file download
 */
export const downloadFile = async (fileId) => {
  console.log('downloadFile called with:', fileId)
  
  // TODO: Call GET /files/:id endpoint
  // TODO: Handle file download
  
  throw new Error('Not implemented')
}

/**
 * Delete a file by ID
 * TODO: Implement file deletion
 */
export const deleteFile = async (fileId) => {
  console.log('deleteFile called with:', fileId)
  
  // TODO: Call DELETE /files/:id endpoint
  // TODO: Require authentication
  
  throw new Error('Not implemented')
}

/**
 * Get shareable link for a file
 * TODO: Implement shareable link generation
 */
export const getShareLink = async (fileId) => {
  console.log('getShareLink called with:', fileId)
  
  // TODO: Call POST /files/:id/share endpoint
  // TODO: Return unique share token
  
  throw new Error('Not implemented')
}
