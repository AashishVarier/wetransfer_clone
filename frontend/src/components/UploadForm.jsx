import { useState } from 'react'
import { uploadFile } from '../services/api'

export default function UploadForm({ onUpload }) {
  const [selectedFile, setSelectedFile] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleFileSelect = (e) => {
    const file = e.target.files[0]
    
    // TODO: Implement 2MB validation
    if (file && file.size > 2 * 1024 * 1024) {
      console.warn('File size exceeds 2MB limit')
      return
    }

    setSelectedFile(file)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!selectedFile) {
      console.warn('No file selected')
      return
    }

    setLoading(true)

    try {
      // TODO: Call actual backend API
      await uploadFile(selectedFile)
      console.log('File uploaded successfully:', selectedFile.name)
      onUpload(selectedFile)
      setSelectedFile(null)
    } catch (error) {
      console.error('Upload failed:', error)
      // TODO: Show error message to user
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <div className="border-2 border-dashed border-blue-300 rounded-lg p-8 text-center hover:border-blue-500 transition">
        <label className="cursor-pointer">
          <input
            type="file"
            onChange={handleFileSelect}
            className="hidden"
            accept="*/*"
          />
          <div className="text-6xl mb-4">📁</div>
          <p className="text-gray-700 font-medium mb-2">
            {selectedFile ? selectedFile.name : 'Click to select a file or drag and drop'}
          </p>
          <p className="text-gray-500 text-sm">
            Maximum file size: 2MB
          </p>
        </label>
      </div>

      <button
        type="submit"
        disabled={!selectedFile || loading}
        className="w-full mt-6 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-bold py-3 px-4 rounded-lg transition"
      >
        {loading ? 'Uploading...' : 'Upload File'}
      </button>
    </form>
  )
}
