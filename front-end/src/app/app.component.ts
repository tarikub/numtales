import { Component } from '@angular/core';
import { StoryServiceService } from './story-service.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  standalone: false,
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'front-end';
  story: any;
  image: any;
  startingStory: number = 0;
  nextDisabled: boolean = false;

  public constructor(private storyService: StoryServiceService) {
    // Constructor logic
  }

  public ngOnInit() {
    this.getNextStory();
  }

  public getNextStory() {
    this.nextDisabled = true;
    this.startingStory++;
    this.storyService.searchStory(this.startingStory.toString()).subscribe(response => {
      // Get the first story from the stories array
      if (response && response.stories && response.stories.length > 0) {
        const matchingStory = response.stories.filter((i: { number: number; }) => i.number == this.startingStory);

        if (matchingStory.length > 0) {
          this.story = matchingStory[0];
          let query = `${this.story.title.toString()} ${this.story.story.toString()}`;
          this.storyService.searchImages(query).subscribe(matchingImage => {
           this.image = matchingImage.images[Math.floor(Math.random() * matchingImage.images.length)];

            this.storyService.getStoryImage(this.image.id).subscribe(imageResponse => {
              // Get the first image from the images array
              if (imageResponse) {
                this.image.url = imageResponse['primaryImage'];
              } else {
                this.image = 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=500&q=80';
              }

               this.nextDisabled = false;
            });
          });
        }

      } else {
        this.story = null;
        console.log('No story found');
      }
    });
  }
}
