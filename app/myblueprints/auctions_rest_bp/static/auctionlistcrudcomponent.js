  const AuctionListCrudComponent = {
    delimiters: ['[[',']]'], // Use other delimiters than default to avoid collision with Jinja2
    data() {
      return {
        // Create varialbes/objects/arrays needed in the vue app
        auctions: [],
        newAuction: {
          id: '',
          description: '',
          starting_bid: '',
          duration: '',
          image_url: ''
        },
        indexEditingAuction: null,
        editedAuction: {
          id: '',
          description: '',
          starting_bid: '',
          duration: '',
          image_url: ''},
        showEditForm: false
      };
    },
    mounted() {
      // Call method like get_rest_data() to get initial data from rest api
      this.fetchAuctions();
    },
    methods: {
      fetchAuctions() {
        axios.get('/api/v1/auctions')
          .then(response => {
            this.auctions = response.data;
          })
          .catch(error => {
            console.error('There was an error fetching the auctions!', error);
          });
      },
      addAuction() {
        axios.post('/api/v1/auctions', this.newAuction)
          .then(response => {
            this.auctions.push(response.data);
            // Clear the form
            this.newAuction = {
              id: '',
              description: '',
              starting_bid: '',
              duration: '',
              image_url: ''
            };
          })
          .catch(error => {
            console.error('There was an error adding the auction!', error);
          });
      },
      editAuction(index) {
        this.showEditForm = true;
        // {...this.auctions[auctionId]} // Like python tuple unpacking,
        // creates a new object by spreading the properties of the existing auction
        // retrieved from this.auctions array into a new object.

        this.editedAuction = { ...this.auctions[index] }; // unpacking used with form editing, v-model used for mappping between textfields and this datamodel, editedAuction
      },
      updateAuction() {
        // Ensure the starting bid is a number before sending the update
        this.editedAuction.starting_bid = Number(this.editedAuction.starting_bid);
        axios.put(`/api/v1/auctions/${this.editedAuction.id}`, this.editedAuction)
          .then(response => {
            const index = this.auctions.findIndex(a => a.id === this.editedAuction.id);
            if (index !== -1) {
              this.auctions[index] = response.data;
            }
            this.showEditForm = false; // Hide the edit form after updating
            for (key in this.editedAuction) {
              this.editedAuction[key] = '';
            }; // Clear the editedAuction object
            console.log(this.editedAuction);
          })
          .catch(error => {
            console.error('There was an error updating the auction!', error);
          });
      },
      deleteAuction(index) {
        axios.delete(`/api/v1/auctions/${this.auctions[index].id}`)
          .then(() => {
            // Remove the auction from the array by its ID
            this.auctions = this.auctions.filter(a => a.id !== this.auctions[index].id);
          })
          .catch(error => {
            console.error('There was an error deleting the auction!', error);
          });
      },
      restorejson() {
        axios.post('/api/v1/auctions/reset')
          .then(response => {
            this.auctions = response.data;
          })
          .catch(error => {
            console.error('There was an error restoring the auctions!', error);
          });
      },
      get_rest_data() {

      }//end get_rest_data

    },
    template: /*html*/`
    <h1>Auktions Vue App</h1>
    <table>
      <tr v-for="(auction,index) in auctions" :key="auction.id">
        <td>[[ auction.id ]] - [[ auction.description ]] - [[ auction.starting_bid ]] - [[ auction.duration ]]</td>
        <td><img :src="auction.image_url" alt="Auction Image" width="100"></td>
        <td><button @click="editAuction(index)">Edit</button></td>
        <td><button @click="deleteAuction(index)">Delete</button></td>
      </tr>
    </table>
    <button @click="restorejson" class="btn btn-primary">Restore json</button>

    <h2>Add Person</h2>
    <form @submit.prevent="addAuction">
      <label for="id">ID:</label>
      <input type="number" v-model="newAuction.id" required><br>

      <label for="description">Description:</label>
      <input type="text" v-model="newAuction.description" required><br>

      <label for="starting_bid">Starting Bid:</label>
      <input type="number" v-model="newAuction.starting_bid" required><br>

      <label for="duration">Auction Duration (days):</label>
      <input type="number" v-model="newAuction.duration" required><br>

      <label for="image_url">Image URL:</label>
      <input type="text" v-model="newAuction.image_url" required><br>

      <button type="submit">Add Auction</button>
    </form>
    <hr>

    <!-- Edit auction -->
    <form v-if="showEditForm === true" @submit.prevent="updateAuction">
      <input type="text" v-model="editedAuction.description" required>
      <input type="number" v-model="editedAuction.starting_bid" required>

      <button type="submit">Update Auction</button>
    </form>

    `,
  };//end of AuctionListCrudComponent