import { error } from '@sveltejs/kit';
import { posts } from '../data.js';

export function load({ params }) {
  const id = Number(params.id);

  const post = posts.find(p => p.id === id);

  if (!post) throw error(404, 'Post not found');

  return { post };
}