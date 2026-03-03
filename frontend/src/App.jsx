import { useState } from 'react'
import UploadForm from './components/UploadForm'
import FileList from './components/FileList'

function App() {
  const [files, setFiles] = useState([])

  const handleUpload = (file) => {
    // TODO: Connect to backend API
    console.log('Uploading file:', file)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            WeTransfer Clone
          </h1>
          <p className="text-gray-600">
            Share files securely and easily
          </p>
        </header>

        <main className="space-y-8">
          <section className="bg-white rounded-lg shadow-lg p-8">
            <UploadForm onUpload={handleUpload} />
          </section>

          <section className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">
              Your Files
            </h2>
            <FileList files={files} />
          </section>
        </main>

        <footer className="text-center text-gray-600 mt-12">
          <p>&copy; 2024 WeTransfer Clone. v1.0.0</p>
        </footer>
      </div>
    </div>
  )
}

export default App
