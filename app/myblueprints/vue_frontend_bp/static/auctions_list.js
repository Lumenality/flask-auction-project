const auctions_api_url = 'http://127.0.0.1:5000/api/v1/auctions';
const user_api_url = 'http://127.0.0.1:5000/api/v1/users';
const current_date = new Date();
const AuctionListCrudComponent = {
  delimiters: ["[[", "]]"],
  data() {
    return {
      auctions: [],
      foundAuctions: [],
      current_user_id: window.currentUserId || null,
      loading: false,
      error: null,
      // Search and filter fields
      searchDescription: "",
      minPrice: null,
      maxPrice: null,
      endDate: new Date(new Date().setDate(new Date().getDate() + 30)).toISOString().split('T')[0] // Default end date 30 days from now
    };
  },
  mounted() {
    this.fetchAuctions();
    console.log("Vue app mounted.");
  },
  methods: {
    fetchAuctions() {
      this.loading = true;
      this.error = null;
      axios
        .get(auctions_api_url)
        .then((response) => {
          this.auctions = response.data;
          this.foundAuctions = response.data; // Initialize foundAuctions
          console.log("Auctions fetched:", this.auctions);
        })
        .catch((error) => {
          this.error = 'Error fetching auctions: ' + error.message;
          console.error("Error fetching auctions:", error);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    fetchUserLikesDislikes() {
      axios
        .get(`${user_api_url}/${this.current_user_id}/likes_dislikes`)
        .then((response) => {
          return response.data;
        });
    },
    likeAuction(auctionId) {
      axios
        .post(`${auctions_api_url}/${auctionId}/like`)
        .then((response) => {
          const auction = this.auctions.find(a => a.id === auctionId);
          if (auction) {
            auction.likes = response.data.likes;
            auction.dislikes = response.data.dislikes;
          }
        })
        .catch((error) => {
          console.error("Error liking auction:", error);
        });
    },
    dislikeAuction(auctionId) {
      axios
        .post(`${auctions_api_url}/${auctionId}/dislike`)
        .then((response) => {
          const auction = this.auctions.find(a => a.id === auctionId);
          if (auction) {
            auction.likes = response.data.likes;
            auction.dislikes = response.data.dislikes;
          }
        })
        .catch((error) => {
          console.error("Error disliking auction:", error);
        });
    },
    viewAuction(auctionId) {
      window.location.href = `/auctions/${auctionId}`;
    },
    applyFilters() { // Extended search method from my däckfirma project
      const search = this.searchDescription || "";
      const filteredAuctions = this.auctions.filter(auction => {
        const matchesDescription = auction.description
          ? auction.description.toLowerCase().includes(search.toLowerCase())
          : true;
        const meetsMin = this.minPrice !== null
          ? auction.highest_bid >= this.minPrice 
          : true;
        const meetsMax = this.maxPrice !== null
          ? auction.highest_bid <= this.maxPrice
          : true;
        const auctionEndDate = Date.parse(auction.end_time);
        const filterEndDate = Date.parse(this.endDate);
        const meetsEndDate = this.endDate
          ? auctionEndDate <= filterEndDate
          : true;
        return matchesDescription && meetsMin && meetsMax && meetsEndDate;
      });
      this.foundAuctions = filteredAuctions;
    },
    clearFilters() {
      this.searchDescription = "";
      this.minPrice = null;
      this.maxPrice = null;
      this.endDate = new Date(new Date().setDate(new Date().getDate() + 30)).toISOString().split('T')[0];
      this.foundAuctions = this.auctions;
    }
  },
  template: /*html*/ `
  <div class="container mt-4">
    <div id="search-container">
      <div id="search-fields">
        <input
          type="text"
          id="description"
          placeholder="Sök auktioner efter beskrivning"
          v-model="searchDescription"
          v-on:input="applyFilters"
        />
      </div>
      <div id="price-filters" class="mt-3">
        <input
          type="number"
          id="min-price"
          placeholder="Min pris"
          v-model.number="minPrice"
          v-on:input="applyFilters"
        />
        <input
          type="number"
          id="max-price"
          placeholder="Max pris"
          v-model.number="maxPrice"
          v-on:input="applyFilters"
        />
      </div>
      <div id="date-filter" class="mt-3">
      <label for="start">Senaste slutdatum:</label>
      
      <input
        type="date"
        id="start"
        name="trip-start"
        v-model="endDate"
        :min="new Date().toISOString().split('T')[0]"
        :value="endDate"
        @input="applyFilters"
        />
      </div>
      <button class="btn btn-primary mt-3" @click="clearFilters">Rensa filter</button>
    </div>
    <div class="row">
      <div v-for="auction in foundAuctions" :key="auction.id" class="col-md-4 mb-4">
        <auctions-card
          :auction="auction"
          @like-auction="likeAuction"
          @dislike-auction="dislikeAuction"
          @view-auction="viewAuction"
        ></auctions-card>
      </div>
    </div>
  </div>

  `,
};