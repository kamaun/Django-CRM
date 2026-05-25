<script>
  import { KanbanBoard } from '$lib/components/ui/kanban';
  import OpportunityCard from './OpportunityCard.svelte';

  /**
   * @typedef {Object} Column
   * @property {string} id
   * @property {string} name
   * @property {number} order
   * @property {string} color
   * @property {string} stage_type
   * @property {boolean} is_status_column
   * @property {number|null} wip_limit
   * @property {number} [item_count]
   * @property {Array<any>} items
   */

  /**
   * @typedef {Object} KanbanData
   * @property {string} mode
   * @property {Object|null} pipeline
   * @property {Column[]} columns
   * @property {number} total_items
   */

  /**
   * @type {{
   *   data: KanbanData | null,
   *   loading?: boolean,
   *   onStageChange: (opportunityId: string, newStage: string, columnId: string, aboveId: string | null, belowId: string | null) => Promise<void>,
   *   onCardClick: (opportunity: any) => void,
   *   onAddItem?: (columnId: string) => void
   * }}
   */
  let { data = null, loading = false, onStageChange, onCardClick, onAddItem } = $props();
</script>

<KanbanBoard
  {data}
  {loading}
  itemName="opportunity"
  itemNamePlural="opportunities"
  onItemMove={onStageChange}
  {onCardClick}
  {onAddItem}
  CardComponent={OpportunityCard}
  emptyMessage="No opportunities in your pipeline"
/>
