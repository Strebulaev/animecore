export interface Genre {
  id: number
  name: string
  slug: string
}

export interface Anime {
  id: number
  title_ru: string
  title_en: string
  title_jp: string
  poster_url: string
  poster_file: string | null
  description: string
  year: number | null
  status: string
  episodes: number | null
  genres: Genre[]
  created_at: string
}

export interface User {
  id: number
  username: string
  email: string
  avatar_url?: string
}

export interface Playlist {
  id: number
  title: string
  description?: string
  is_public: boolean
  items: PlaylistItem[]
  user: User
}

export interface PlaylistItem {
  id: number
  anime: Anime
  source_url: string
  episode?: number
  note?: string
}