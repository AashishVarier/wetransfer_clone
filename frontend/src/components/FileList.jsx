import { useEffect, useState } from 'react'
import { listFiles } from '../services/api'

export default function FileList({ files: initialFiles }) {
  const [files, setFiles] = useState(initialFiles)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    // TODO: Fetch files from backend API on component mount
    const fetchFiles = async () => {
      setLoading(true)
      try {
        const data = await listFiles()
        setFiles(data)
      } catch (error) {
        console.error('Failed to fetch files:', error)
      } finally {
        setLoading(false)
      }
    }

    // Uncomment when API is ready:
    // fetchFiles()
  }, [])

  // Mock data for demonstration
  const mockFiles = [
    { id: 1, name: 'example.pdf', size: '1.2 MB', uploadedAt: '2024-01-15', link: 'https://example.com/share/abc123' },
    { id: 2, name: 'image.jpg', size: '0.8 MB', uploadedAt: '2024-01-14', link: 'https://example.com/share/def456' },
  ]

  const displayFiles = files.length > 0 ? files : mockFiles

  if (loading) {
    return <p className="text-gray-500">Loading files...</p>
  }

  return (
    <div>
      {displayFiles.length === 0 ? (
        <p className="text-gray-500 text-center py-8">
          No files uploaded yet. Upload one to get started!
        </p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-gray-700">
            <thead className="bg-gray-100 border-b">
              <tr>
                <th className="px-4 py-3 font-semibold">File Name</th>
                <th className="px-4 py-3 font-semibold">Size</th>
                <th className="px-4 py-3 font-semibold">Uploaded</th>
                <th className="px-4 py-3 font-semibold">Share Link</th>
              </tr>
            </thead>
            <tbody>
              {displayFiles.map((file) => (
                <tr key={file.id} className="border-b hover:bg-gray-50">
                  <td className="px-4 py-3">{file.name}</td>
                  <td className="px-4 py-3">{file.size}</td>
                  <td className="px-4 py-3">{file.uploadedAt}</td>
                  <td className="px-4 py-3">
                    <a
                      href={file.link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:underline"
                    >
                      Share
                    </a>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
