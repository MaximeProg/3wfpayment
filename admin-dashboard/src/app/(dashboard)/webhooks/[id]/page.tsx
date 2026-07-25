import { WebhookDetailClient } from "./detail-client";

export default async function WebhookDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return <WebhookDetailClient id={id} />;
}
