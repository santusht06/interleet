/*
 * Copyright 2026 Sharexpress Contributors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import { useEffect, useState } from "react";
import { API } from "@/api/api";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { ThumbsUp, Lock, MessageSquare, Loader2 } from "lucide-react";
import { toast } from "sonner";

export function DiscussionPanel({ slug }) {
  const [discussions, setDiscussions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [content, setContent] = useState("");
  const [posting, setPosting] = useState(false);

  const [editorial, setEditorial] = useState(null);
  const [editorialLocked, setEditorialLocked] = useState(false);
  const [editorialLoading, setEditorialLoading] = useState(false);
  const [editorialLoaded, setEditorialLoaded] = useState(false);

  const loadDiscussions = async () => {
    setLoading(true);
    try {
      const res = await API.get(`/api/challenges/${slug}/discussions`);
      setDiscussions(res.data?.discussions || []);
    } catch {
      // list is best-effort; leave empty on failure
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (slug) loadDiscussions();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [slug]);

  const submitComment = async () => {
    const text = content.trim();
    if (!text) return;
    setPosting(true);
    try {
      await API.post(`/api/challenges/${slug}/discussions`, { content: text });
      setContent("");
      await loadDiscussions();
    } catch (err) {
      const status = err?.response?.status;
      toast.error(
        status === 401
          ? "Log in to post a comment."
          : err?.response?.data?.detail || "Failed to post comment."
      );
    } finally {
      setPosting(false);
    }
  };

  const upvote = async (id) => {
    try {
      const res = await API.post(`/api/discussions/${id}/upvote`);
      setDiscussions((prev) =>
        prev.map((d) => (d.id === id ? { ...d, upvotes: res.data?.upvotes ?? d.upvotes } : d))
      );
    } catch (err) {
      toast.error(err?.response?.status === 401 ? "Log in to upvote." : "Failed to upvote.");
    }
  };

  const loadEditorial = async () => {
    if (editorialLoaded) return;
    setEditorialLoading(true);
    try {
      const res = await API.get(`/api/challenges/${slug}/editorial`);
      setEditorial(res.data?.editorial || null);
      setEditorialLocked(false);
    } catch (err) {
      if (err?.response?.status === 403) {
        setEditorialLocked(true);
      } else {
        toast.error(err?.response?.data?.detail || "Failed to load editorial.");
      }
    } finally {
      setEditorialLoading(false);
      setEditorialLoaded(true);
    }
  };

  return (
    <Card className="border-border bg-card p-6">
      <Tabs
        defaultValue="discussion"
        onValueChange={(v) => {
          if (v === "editorial") loadEditorial();
        }}
      >
        <TabsList>
          <TabsTrigger value="discussion">
            <MessageSquare className="mr-1.5 h-4 w-4" /> Discussion
          </TabsTrigger>
          <TabsTrigger value="editorial">
            <Lock className="mr-1.5 h-4 w-4" /> Editorial
          </TabsTrigger>
        </TabsList>

        <TabsContent value="discussion" className="mt-4 space-y-4">
          <div className="space-y-2">
            <Textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="Share your approach, ask a question…"
              rows={3}
            />
            <div className="flex justify-end">
              <Button onClick={submitComment} disabled={posting || !content.trim()}>
                {posting ? <Loader2 className="mr-1.5 h-4 w-4 animate-spin" /> : null}
                Post
              </Button>
            </div>
          </div>

          {loading ? (
            <p className="text-sm text-muted-foreground">Loading discussion…</p>
          ) : discussions.length === 0 ? (
            <p className="text-sm text-muted-foreground">
              No comments yet. Be the first to start the discussion.
            </p>
          ) : (
            <ul className="space-y-3">
              {discussions.map((d) => (
                <li key={d.id} className="rounded-lg border border-border bg-background/50 p-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">{d.username}</span>
                    <button
                      type="button"
                      onClick={() => upvote(d.id)}
                      className="inline-flex items-center gap-1 text-xs text-muted-foreground hover:text-primary"
                    >
                      <ThumbsUp className="h-3.5 w-3.5" /> {d.upvotes ?? 0}
                    </button>
                  </div>
                  <p className="mt-1.5 whitespace-pre-wrap text-sm text-foreground/85">{d.content}</p>
                </li>
              ))}
            </ul>
          )}
        </TabsContent>

        <TabsContent value="editorial" className="mt-4">
          {editorialLoading ? (
            <p className="text-sm text-muted-foreground">Loading editorial…</p>
          ) : editorialLocked ? (
            <div className="flex flex-col items-center gap-2 rounded-lg border border-dashed border-border py-10 text-center">
              <Lock className="h-6 w-6 text-muted-foreground" />
              <p className="text-sm font-medium">Editorial locked</p>
              <p className="text-xs text-muted-foreground">
                Solve this problem to unlock the official solution.
              </p>
            </div>
          ) : editorial ? (
            <div className="space-y-3">
              {editorial.description ? (
                <p className="text-sm text-foreground/85">{editorial.description}</p>
              ) : null}
              {editorial.language ? (
                <span className="text-xs uppercase tracking-wide text-muted-foreground">
                  {editorial.language}
                </span>
              ) : null}
              <pre className="max-h-[480px] overflow-auto rounded-lg border border-border bg-background/70 p-4 text-xs">
                <code>{editorial.code}</code>
              </pre>
            </div>
          ) : (
            <p className="text-sm text-muted-foreground">Open this tab to load the editorial.</p>
          )}
        </TabsContent>
      </Tabs>
    </Card>
  );
}
