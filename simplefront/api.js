/* global APP_CONFIG */

// This file contains every HTTP request sent to the FastAPI backend.
window.articleApi = (() => {
  /**
   * Sends a request to FastAPI and returns its JSON response.
   */
  async function request(path, options = {}) {
    const url = APP_CONFIG.apiUrl + path
    const method = options.method || 'GET'
    let response

    console.info(`[API] ${method} ${url}`)

    try {
      response = await fetch(url, {
        ...options,
        headers: {
          Accept: 'application/json',
          ...(options.body ? { 'Content-Type': 'application/json' } : {}),
          ...options.headers,
        },
      })
    } catch (cause) {
      console.error(
        `[API] The ${method} request to ${url} was blocked or failed.`,
        cause,
      )
      throw new Error(
        `Unable to reach FastAPI at ${APP_CONFIG.apiUrl}. ` +
          'If FastAPI reports status 200, check its CORS configuration.',
      )
    }

    console.info(`[API] Response ${response.status} for ${method} ${url}`)

    if (!response.ok) {
      // FastAPI usually returns errors as { "detail": "..." }.
      const body = await response.json().catch(() => null)
      const detail = body?.detail
      let message = `HTTP error ${response.status}`

      if (typeof detail === 'string') {
        message = detail
      } else if (detail) {
        message = JSON.stringify(detail)
      }

      console.error(`[API] ${message}`, body)
      const error = new Error(message)
      error.status = response.status
      throw error
    }

    // A 204 response never contains a body.
    if (response.status === 204) return null

    try {
      const text = await response.text()
      return text ? JSON.parse(text) : null
    } catch (cause) {
      console.error(`[API] The response from ${url} is not valid JSON.`, cause)
      throw new Error('FastAPI responded, but its response is not valid JSON.')
    }
  }

  /**
   * Fetches the article list.
   */
  function list() {
    return request('/list')
  }

  /**
   * Fetches one article from its URL.
   */
  function get(articleUrl) {
    return request(`/article/${encodeURIComponent(articleUrl)}`)
  }

  /**
   * Creates an article from its name and Markdown content.
   */
  function create(article) {
    return request('/create', {
      method: 'POST',
      body: JSON.stringify(article),
    })
  }

  /**
   * Updates Markdown content and optional article metadata.
   */
  function update(articleUrl, article) {
    return request(`/article/${encodeURIComponent(articleUrl)}/edit`, {
      method: 'POST',
      body: JSON.stringify(article),
    })
  }

  /** Fetches comments for the whole site. */
  function listComments() {
    return request('/comments')
  }

  /** Publishes a comment and returns the stored comment. */
  function createComment(comment) {
    return request('/comments', {
      method: 'POST',
      body: JSON.stringify(comment),
    })
  }

  /** Calls the course API's GET deletion route. Never cache this request. */
  function remove(articleUrl) {
    return request(`/article/${encodeURIComponent(articleUrl)}/delete`, {
      method: 'GET',
      cache: 'no-store',
    })
  }

  return { list, get, create, update, remove, listComments, createComment }
})()
